import re
import openai
from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import random
import pandas as pd
from datetime import datetime

# Configuration for OpenAI
openai.api_key = "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"

# Load data from an Excel file for the application's backend processing
data = pd.read_excel("PIT_data_full.xlsx")

# Constants for default values used in calculations
DEFAULT_CVa = 1
DEFAULT_CVp = 1
SOME_THRESHOLD = 30  # Threshold for acceptable wait time in seconds
ACTIVITY_TIMES = {'ID Inspection': 15, 'Carry-on': 40, 'AIT': 15, 'Pat-down': 10}

# Function to calculate waiting time at each checkpoint
def calculate_waiting_time(arrival_rate, CVa, CVp, activity_time):
    if arrival_rate == 0:
        return None, "Error: Arrival rate cannot be zero."
    A = (1 / arrival_rate) * 60
    utilization = activity_time / A
    if utilization >= 1:
        return None, "Error: Utilization is 100% or more, system is overloaded."
    utilization_factor = utilization / (1 - utilization)
    waiting_time = activity_time * utilization_factor * ((CVa ** 2 + CVp ** 2) / 2)
    return waiting_time, f"Estimated waiting time: {waiting_time:.2f} seconds"

# Function to calculate new waiting times with additional staff
def calculate_total_waiting_time(staff_allocation, people_count, updated_times):
    total_waiting_time = 0
    for checkpoint, staff_count in staff_allocation.items():
        # Ensure at least one staff member
        staff_count = max(staff_count, 1)
        waiting_time, _ = calculate_waiting_time(people_count / 60, DEFAULT_CVa, DEFAULT_CVp, updated_times[checkpoint] / staff_count)
        total_waiting_time += waiting_time if waiting_time is not None else 0
    return total_waiting_time

# Function to allocate staff across different checkpoints
def allocate_staff(staff_count, people_count, updated_times):
    if staff_count == 0:
        return "No additional staff available for allocation."

    allocated_staff = {checkpoint: 1 for checkpoint in updated_times}

    # Identify initial bottlenecks
    bottleneck_checkpoints = []
    for checkpoint in updated_times:
        time, _ = calculate_waiting_time(people_count / 60, DEFAULT_CVa, DEFAULT_CVp, updated_times[checkpoint])
        if time is None:
            bottleneck_checkpoints.append(checkpoint)

    while staff_count > 0:
        for checkpoint in bottleneck_checkpoints:
            if staff_count > 0:
                allocated_staff[checkpoint] += 1
                staff_count -= 1
                new_time, _ = calculate_waiting_time(people_count / 60, DEFAULT_CVa, DEFAULT_CVp, updated_times[checkpoint] / allocated_staff[checkpoint])
                if new_time is not None:
                    bottleneck_checkpoints.remove(checkpoint)

        if not bottleneck_checkpoints:
            break

    # Allocate remaining staff
    while staff_count > 0:
        checkpoint_to_allocate = max(updated_times, key=lambda cp: calculate_waiting_time(people_count / 60, DEFAULT_CVa, DEFAULT_CVp, updated_times[cp] / allocated_staff[cp])[0])
        allocated_staff[checkpoint_to_allocate] += 1
        staff_count -= 1

    # Check for unresolved bottlenecks
    for checkpoint, staff in allocated_staff.items():
        waiting_time, _ = calculate_waiting_time(people_count / 60, DEFAULT_CVa, DEFAULT_CVp, updated_times[checkpoint] / staff)
        if waiting_time is None:
            # If any bottleneck remains unresolved, return the message directly
            return "We need more employees due to bottleneck issues. Please call more in!"

    # If there are no unresolved bottlenecks, return the allocation summary
    allocation_summary = [f"{staff - 1} additional staff member(s) added to {checkpoint}" for checkpoint, staff in allocated_staff.items() if staff > 1]
    total_final_time = sum(calculate_waiting_time(people_count / 60, DEFAULT_CVa, DEFAULT_CVp, updated_times[checkpoint] / staff)[0] for checkpoint, staff in allocated_staff.items())
    allocation_summary.append(f"Total waiting time changed to {total_final_time:.2f} seconds.")

    return "Optimal staff allocation to reduce waiting time:\n" + "\n".join(allocation_summary)

# Function to calculate weighted waiting time reduction for a given checkpoint
def calculate_weighted_waiting_time_reduction(checkpoint, staff_allocation, people_count, updated_times):
    current_time, _ = calculate_waiting_time(people_count / 60, DEFAULT_CVa, DEFAULT_CVp, updated_times[checkpoint] / staff_allocation[checkpoint])
    current_time = current_time if current_time is not None else float('inf')

    new_time, _ = calculate_waiting_time(people_count / 60, DEFAULT_CVa, DEFAULT_CVp, updated_times[checkpoint] / (staff_allocation[checkpoint] + 1))
    new_time = new_time if new_time is not None else float('inf')

    time_reduction = current_time - new_time
    return time_reduction * updated_times[checkpoint]

# Function to calculate new waiting times after staff reallocation
def calculate_new_waiting_times(staff_allocation, people_count, updated_times):
    new_waiting_times = {}
    for checkpoint, staff_count in staff_allocation.items():
        staff_count = max(staff_count, 1)  # Ensure at least one staff member
        waiting_time, _ = calculate_waiting_time(people_count / 60, DEFAULT_CVa, DEFAULT_CVp, updated_times[checkpoint] / staff_count)
        new_waiting_times[checkpoint] = waiting_time if waiting_time is not None else float('inf')
    return new_waiting_times

# Function to calculate additional capacity needed at each checkpoint
def calculate_additional_capacity_needed(activity_time, arrival_rate):
    # Start with the assumption of 1 staff member
    current_staff = 1
    while True:
        # Calculate new utilization with the current staff count
        new_activity_time = activity_time / current_staff
        A = (1 / arrival_rate) * 60
        new_utilization = new_activity_time / A

        # If utilization is below 100%, return the number of additional staff needed
        if new_utilization < 1:
            # Subtracting 1 because we started with 1 staff
            return current_staff - 1
        else:
            # Increment staff count and recheck
            current_staff += 1

# Function to generate prompt for OpenAI GPT based on user input
def generate_prompt(question):
    question = question.lower()

    if 'waiting time' in question and 'people' in question:
        num_people = int(''.join(filter(str.isdigit, question)))
        return f"Calculate the waiting time for {num_people} people at an airport using Little's Law."

    elif 'allocate staff' in question or 'sitting around' in question:
        match_people = re.search(r'\d+ people', question)
        match_staff = re.search(r'\d+ staff', question)
        if match_people and match_staff:
            people_count = int(match_people.group().split()[0])
            staff_count = int(match_staff.group().split()[0])
            allocation = allocate_staff(staff_count, people_count)
            return f"Optimal allocation to reduce waiting time: {allocation}"

    return f"Please provide an analysis for the following query: {question}"

# Generate a random greeting for the application's UI
def greeting():
    greetings = ["Hello! How can I assist you today?", "Hi there! What can I do for you?", "Greetings! What do you need help with?"]
    return random.choice(greetings)

# Dropdown options for various selections in the application's front end
airport_options = [{'label': airport, 'value': airport} for airport in data['Airport'].unique()]
date_options = [{'label': date.strftime('%Y-%m-%d'), 'value': date.strftime('%Y-%m-%d')} for date in data['Date'].dt.date.unique()]
entrance_options = [{'label': entrance, 'value': entrance} for entrance in data['Entrance'].unique()]
time_options = [{'label': time, 'value': time} for time in data['Hour of Day'].unique()]
time_options = sorted(time_options, key=lambda x: datetime.strptime(x['value'], '%H:%M'))
dropdown_airport = dcc.Dropdown(id='dropdown-airport', options=airport_options, placeholder='Select Airport')
dropdown_date = dcc.Dropdown(id='dropdown-date', options=date_options, placeholder='Select Date')
dropdown_entrance = dcc.Dropdown(id='dropdown-entrance', options=entrance_options, placeholder='Select Entrance')
dropdown_time = dcc.Dropdown(id='dropdown-time', options=time_options, placeholder='Select Time')

# Instantiate the Dash app
app = Dash(__name__, external_stylesheets=[
    dbc.themes.LUX,
    '/assets/custom.css'
])

# Different ChatGPT model options displayed on the front end
model_options = ['text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001', 'text-davinci-002', 'text-davinci-001']

# Questions and Answers for the FAQ section
faqs = [
    {
        "question": "How should I phrase my question to calculate waiting times?",
        "answer": "To calculate waiting times, phrase your question with specific details such as the number of people and the checkpoint. For example, 'What is the waiting time for 50 people?'"
    },
    {
        "question": "What kind of questions can I ask about staff allocation?",
        "answer": "Ask questions about staff allocation by specifying the number of staff and passengers. For instance, you might ask, 'We have 5 staff SITTING AROUND, how can we best ALLOCATE the staff for 100 passengers?'"
    },
    {
        "question": "What is a bottleneck?",
        "answer": "A bottleneck in this context refers to a point in the airport security process where the flow of passengers is restricted, leading to increased waiting times."
    },
    {
        "question": "What is Little's Law?",
        "answer": "Little's Law is a theorem used in queueing theory stating that the long-term average number of customers in a stationary system is equal to the long-term average effective arrival rate multiplied by the average time a customer spends in the system."
    },
    {
        "question": "How does the chatbot calculate waiting times?",
        "answer": "The chatbot calculates waiting times based on input data like the number of passengers and staff, and the activity times for different checkpoints. It uses queueing theory principles and algorithms to estimate wait times and suggest optimal staff allocation."
    },
    {
        "question": "What factors influence airport security wait times?",
        "answer": "Several factors influence wait times, including the number of active checkpoints, staff availability, the arrival rate of passengers, and the efficiency of security procedures. Seasonal variations and special events can also impact the flow of passengers."
    },
    {
        "question": "Can the chatbot help in optimizing staff allocation?",
        "answer": "Yes, the chatbot can suggest optimal staff allocation based on the current passenger flow and the activity times at different checkpoints. It aims to minimize bottlenecks and reduce overall waiting times."
    },
    {
        "question": "What is the purpose of activity times in the context of this application?",
        "answer": "Activity times refer to the estimated time taken for each step in the airport security process, like ID inspection, carry-on scanning, etc. Accurate activity times help in predicting queue lengths and wait times more precisely."
    },
    {
        "question": "How can I use the chatbot to improve airport security efficiency?",
        "answer": "You can use the chatbot to analyze current passenger flow and wait times, identify bottlenecks, and receive recommendations on staff allocation or changes in procedures to improve overall efficiency and passenger experience."
    },
    {
        "question": "What should I do if the system shows 100% utilization?",
        "answer": "100% utilization indicates a system overload, meaning the current resources are insufficient to handle the passenger flow. In such cases, consider increasing staff, opening more checkpoints, or optimizing existing procedures."
    }
]

# Creating the FAQ buttons
def generate_faq_content(faqs):
    return html.Div(
        [html.Div([
            html.Strong(faq["question"]),
            html.Br(),
            faq["answer"]],
            className="my-2") for faq in faqs],
        style={'maxHeight': '300px', 'overflowY': 'auto'}
    )

activity_time_options = [{'label': f'{i} seconds', 'value': i} for i in range(5, 61, 5)]

# Creating the dropdowns for checkpoint activity time customization front end.
checkpoint_dropdowns = dbc.Row(
    [
        dbc.Col(
            [
                html.Label(f"{checkpoint}:", className='mt-2', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id=f'dropdown-{checkpoint.replace(" ", "-").lower()}',
                    options=activity_time_options,
                    value=ACTIVITY_TIMES[checkpoint],
                    style={'width': '100%', 'marginBottom': '10px'}
                )
            ],
            width=3
        ) for checkpoint in ACTIVITY_TIMES.keys()
    ],
    className='mb-3'
)

# Creating the Front End Design
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H2(greeting(), className='text-center mt-4'),  # Greeting message at the top
            width=12
        )
    ),
    dbc.Row(
        dbc.Col(
            html.Img(
                src='https://fly2pie.com/images/default-source/logos/government-logos/tsa-logo.png',
                height='100px',
                style={'marginTop': '15px', 'marginBottom': '15px'}
            ),
            className='text-center'
        )
    ),
    dbc.Row(
        dbc.Col(
            html.Div(
                [
                    html.H1("TSA WAIT TIME CHATBOT", className='title'),
                    html.Img(src='/assets/QuestionMark.png', id="faq-button", className="faq-button", style={"cursor": "pointer"}),
                ],
                className='title-and-button'
            ),
            width=12, align='center'
        )
    ),
    dbc.Popover(
        generate_faq_content(faqs),
        id="faq-popover",
        target="faq-button",
        trigger="focus"
    ),
    dbc.Row([
        dbc.Col([
            dcc.Input(
                id='input-text',
                type='text',
                placeholder='Ask your question here',
                style={
                    'width': '100%',
                    'borderRadius': '15px',
                    'padding': '10px',
                    'marginBottom': '10px',
                    'boxShadow': '2px 2px 2px lightgrey'
                },
                className='mb-3'
            ),
            html.Label("Choose a Model:", className='mt-2', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='models',
                options=[{'label': model, 'value': model} for model in model_options],
                value=model_options[0],  # default value
                style={'borderRadius': '15px', 'boxShadow': '2px 2px 2px lightgrey'},
                className='mb-3'
            ),

            html.Label("Set Activity Times:", className='mt-2', style={'fontWeight': 'bold'}),
            checkpoint_dropdowns,

            html.Button(
                'Submit',
                id='submit-button',
                n_clicks=0,
                className='btn btn-primary mt-2',
                style={
                    'borderRadius': '15px',
                    ':hover': {
                        'backgroundColor': 'lightblue',
                        'borderColor': 'blue'
                    }
                }
            )
        ], width={"size": 6, "offset": 3})
    ]),

    dbc.Row(
        dbc.Col(
            dcc.Loading(
                html.Div(
                    id='output-text',
                    className='text-center mt-4 p-3',
                    style={
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': '15px',
                        'border': '1px solid #e1e1e1',
                        'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '1.2rem',
                        'color': '#212529'
                    }
                ),
                type="circle",
                color="#00BFFF"
            ),
            width=12
        ),
        justify="center",
        className='my-5'
    ),
    html.Div([
        dbc.Row([
            dbc.Col(dropdown_airport, width={"size": 3, "offset": 1}),
            dbc.Col(dropdown_date, width=2),
            dbc.Col(dropdown_entrance, width=2),
            dbc.Col(dropdown_time, width=2),
            dbc.Col(html.Button('Calculate Waiting Time', id='calculate-waiting-time-button'), width=2)
        ], className='mt-4'),
        dbc.Row(
            dbc.Col(
                html.Div(id='waiting-time-output', className='text-center mt-4 p-3'),
                width=12
            ), justify="center", className='my-5'
        )
    ], id='new-functionality-section')
], fluid=True)

@app.callback(
    Output('faq-popover', 'is_open'),
    [Input('faq-button', 'n_clicks')],
    [State('faq-popover', 'is_open')]
)

# Function to make the FAQs pop up once the button is clicked in the front end
def toggle_faq_popover(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Callbacks for Dash components to interact with the user inputs and provide outputs
@app.callback(
    Output('output-text', 'children'),
    [Input('submit-button', 'n_clicks')] + [State(f'dropdown-{checkpoint.replace(" ", "-").lower()}', 'value') for checkpoint in ACTIVITY_TIMES.keys()],
    State('input-text', 'value'),
    State('models', 'value')
)

def update_output(n_clicks, *args):
    # Determine the input that triggered the callback
    trigger = callback_context.triggered[0]['prop_id'].split('.')[0]

    # Unpack args: First the checkpoint times, then the input text and model
    checkpoint_times = args[:len(ACTIVITY_TIMES)]
    text_input, model_input = args[len(ACTIVITY_TIMES):]

    # Update ACTIVITY_TIMES based on user input from the dropdowns
    updated_activity_times = ACTIVITY_TIMES.copy()
    for i, checkpoint in enumerate(ACTIVITY_TIMES.keys()):
        if checkpoint_times[i] is not None:
            updated_activity_times[checkpoint] = checkpoint_times[i]

    # Logic when the submit button is clicked
    if n_clicks > 0 and trigger == 'submit-button':
        # Improved keyword detection for staff allocation
        if any(keyword in text_input.lower() for keyword in ['allocate staff', 'sitting around', 'best way to allocate', 'resources']):
            match_people = re.search(r'(\d+) (passengers|people)', text_input)
            match_staff = re.search(r'(\d+) (staff|employees)', text_input)
            if match_people and match_staff:
                people_count = int(match_people.group(1))
                staff_count = int(match_staff.group(1))
                allocation_result = allocate_staff(staff_count, people_count, updated_activity_times)
                return allocation_result
            else:
                return "Please provide the number of passengers and staff to suggest the best allocation."

        # Handling "waiting time" questions
        elif 'waiting time' in text_input.lower():
            num_people = int(''.join(filter(str.isdigit, text_input)))
            arrival_rate = num_people / 60

            bottleneck_info = {}
            total_waiting_time = 0
            for checkpoint, activity_time in updated_activity_times.items():
                waiting_time, message = calculate_waiting_time(arrival_rate, DEFAULT_CVa, DEFAULT_CVp, activity_time)

                if waiting_time is None:
                    additional_capacity = calculate_additional_capacity_needed(activity_time, arrival_rate)
                    bottleneck_info[checkpoint] = additional_capacity

            # Recalculate waiting times considering additional capacity
            for checkpoint, activity_time in updated_activity_times.items():
                if checkpoint in bottleneck_info:
                    new_activity_time = activity_time / (1 + bottleneck_info[checkpoint])
                    new_waiting_time, _ = calculate_waiting_time(arrival_rate, DEFAULT_CVa, DEFAULT_CVp, new_activity_time)
                else:
                    new_waiting_time, _ = calculate_waiting_time(arrival_rate, DEFAULT_CVa, DEFAULT_CVp, activity_time)

                total_waiting_time += new_waiting_time if new_waiting_time is not None else 0

            bottleneck_messages = [
                f"There's a bottleneck at {checkpoint}. Additional capacity needed: {additional_capacity}." for
                checkpoint, additional_capacity in bottleneck_info.items()]
            bottleneck_message_str = " ".join(bottleneck_messages)
            return f"{bottleneck_message_str} New Total Waiting Time: {total_waiting_time:.2f} seconds"

        # Use GPT model for other queries
        else:
            response = openai.Completion.create(
                model=model_input,
                prompt=f"{text_input}\n",
                max_tokens=400
            )
            generated_text = response.choices[0].text.strip()
            return generated_text

    # Default message when there's no input or action
    return "Please enter a query to get started."


# Callback for calculating waiting time based on user-selected options. This function is linked to the pandas dataset that was imported
@app.callback(
    Output('waiting-time-output', 'children'),
    [Input('calculate-waiting-time-button', 'n_clicks')],
    [State('dropdown-airport', 'value'),
     State('dropdown-date', 'value'),
     State('dropdown-entrance', 'value'),
     State('dropdown-time', 'value')]
)
def calculate_waiting_time_callback(n_clicks, airport, date, entrance, time):
    if n_clicks is None or any(v is None for v in [airport, date, entrance, time]):
        return "Please select all options to calculate the waiting time."

    selected_date = pd.to_datetime(date)
    filtered_data = data[
        (data['Airport'] == airport) &
        (pd.to_datetime(data['Date']).dt.date == selected_date.date()) &
        (data['Entrance'] == entrance) &
        (data['Hour of Day'] == time)
    ]

    if filtered_data.empty:
        return "No data available for the selected options."

    num_passengers = filtered_data.iloc[0]['Total Passengers']
    arrival_rate = num_passengers / 60  # Convert to passengers per minute

    # Determine additional staff needed and recalculate waiting times
    additional_staff_needed = {}
    new_activity_times = ACTIVITY_TIMES.copy()
    for checkpoint in ACTIVITY_TIMES:
        current_waiting_time, _ = calculate_waiting_time(arrival_rate, DEFAULT_CVa, DEFAULT_CVp, ACTIVITY_TIMES[checkpoint])
        if current_waiting_time is None or current_waiting_time > SOME_THRESHOLD:
            additional_staff_needed[checkpoint] = calculate_additional_capacity_needed(ACTIVITY_TIMES[checkpoint], arrival_rate)
            new_activity_times[checkpoint] = ACTIVITY_TIMES[checkpoint] / (1 + additional_staff_needed[checkpoint])
        else:
            new_activity_times[checkpoint] = ACTIVITY_TIMES[checkpoint]

    # Calculate new total waiting time with additional staff
    total_waiting_time = 0
    for checkpoint, activity_time in new_activity_times.items():
        waiting_time, _ = calculate_waiting_time(arrival_rate, DEFAULT_CVa, DEFAULT_CVp, activity_time)
        total_waiting_time += waiting_time if waiting_time is not None else 0

    bottleneck_message = " ".join([f"Bottleneck at {checkpoint}, additional staff needed: {staff}."
                                   for checkpoint, staff in additional_staff_needed.items()])
    return f"{bottleneck_message} New Total Waiting Time: {total_waiting_time:.2f} seconds."

# Main entry point to run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)