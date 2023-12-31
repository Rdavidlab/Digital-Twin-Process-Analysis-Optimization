# Digital-Twin-Process-Analysis-Optimization
A Comprehensive Full-Scale Digital Twin Model for Enhancing Airport Security Checkpoint Efficiency

## Introduction

This project, conducted at Carnegie Mellon University, focuses on optimizing the operations of the Transportation Security Administration (TSA) at national airports, with a particular emphasis on enhancing the security screening process. The TSA, established under the Aviation and Transportation Security Act of 2001, plays a pivotal role in ensuring the security of national transportation systems while facilitating the smooth movement of people and commerce. Balancing the critical needs for security and operational efficiency, this project addresses the prominent challenges in TSA security check processes, particularly in queue management and passenger throughput.

The research integrates advanced technological solutions, exploring the application of Digital Twin technology for modeling TSA queue dynamics and capacity analysis. This technology is aimed at forecasting capacities and managing passenger flow more effectively, thereby enhancing traveler satisfaction and the timeliness of flights. In conjunction with Digital Twin technology, the project investigates the integration of Google's Large Language Model (LLM) PaLM 2 and its associated MakerSuite platform. These computational tools assist in transforming Operations Management models into machine-readable formats, thereby enhancing the Digital Twin framework.

Two specific use cases of the PaLM are explored: codifying existing Operations Management models for automation and developing a user-friendly platform for end-users to interact with the Digital Twin system. This allows for informed decisions based on the underlying queue management processes.

Building on previous work that established the feasibility of conceptualizing the airport screening process within a Digital Twin framework, this project presents a prototypical full-stack Digital Twin implementation, including a fully functioning front-end and back-end. The implementation centers around a question-answering (QA) system designed to improve human-computer interaction and ease of use. By merging theoretical perspectives from Operations Management with practical applications of generative AI and Digital Twin technologies, this report aims to contribute to the literature on optimizing TSA operations and highlights new directions for research in domain-specific applications of advanced computational models.


## Abstract

This study introduces a novel approach to enhancing airport security checkpoint efficiency through the development of a full-scale Digital Twin model. The primary objective is to streamline TSA operations by accurately simulating and analyzing the dynamics of security checkpoints. Utilizing the power of Digital Twin technology, combined with Google's PaLM 2 Large Language Model and MakerSuite platform, the project offers a groundbreaking solution to the perennial challenges faced in airport security management.

The model developed in this project provides a virtual representation of airport security processes, enabling real-time analysis and optimization of passenger flow and resource allocation. The integration of PaLM 2 serves a dual purpose: first, to automate the conversion of Operations Management models into actionable data formats, and second, to facilitate a user-friendly interface for TSA personnel and stakeholders. This advanced approach allows for predictive analytics and scenario planning, equipping airport authorities with the tools to make data-driven decisions and enhance overall airport efficiency.

The results demonstrate the model's capability in improving queue management, reducing wait times, and elevating the passenger experience while maintaining rigorous security standards. This research signifies a transformative step in airport security operations, proposing a scalable and adaptable framework that can be applied to various airport environments.


## Project Team Members

 - Raymond David
 - Sean Park
 - Hyoju Kang
 - Shaun Ho
 - Jinny Kim

## University Affiliation

This project was developed as part of a course project at Carnegie Mellon University, renowned for its pioneering research and innovation. The university provided an interdisciplinary academic setting, essential resources, and expert guidance, facilitating the successful execution of this initiative. Faculty and students across various departments collaborated, embodying the university's emphasis on cross-disciplinary learning and application. This venture underscores Carnegie Mellon's commitment to integrating academic exploration with real-world applications, particularly in fields like artificial intelligence and operations management. The project reflects the university's ethos of harnessing technology for societal advancement, with a specific focus on enhancing national security and transportation efficiency.

## Report Summary

This report presents a comprehensive examination of a full-scale Digital Twin model designed to optimize airport security checkpoint operations. The project's cornerstone is the innovative application of Digital Twin technology, complemented by Google's PaLM 2 Large Language Model and ChatGPT. The model serves as a sophisticated virtual representation of the airport security process, enabling real-time simulation, analysis, and optimization of passenger flow and TSA resource management.

Key highlights of the report include:

- Digital Twin Technology: A deep dive into how this technology provides a dynamic, real-time replica of TSA operations, offering insights into passenger flow and resource optimization.

- Integration with PaLM 2 and MakerSuite: The utilization of advanced AI and machine learning tools for automating data processing and enhancing user interaction with the Digital Twin system.

- Model Development and Implementation: Insight into the creation of a prototype that blends theoretical models from Operations Management with practical AI applications, demonstrating the system's usability and effectiveness.

- Impact Analysis: Evaluation of the model's effectiveness in improving TSA queue management, reducing wait times, and enhancing the overall passenger experience, while upholding stringent security protocols.

- Scalability and Adaptability: Discussion on how the model can be tailored to various airport settings, ensuring wide applicability and scalability.

- Future Directions and Potential Applications: Exploration of how this model could be expanded and adapted for broader applications in airport and transportation management.

## Project Goals

The primary goals of this project were to address and resolve key challenges in airport security checkpoint operations using a full-scale Digital Twin model. The objectives were carefully crafted to ensure significant improvements in TSA processes, with a focus on efficiency, security, and passenger experience. The following are the main goals of the project:

- Enhance Queue Management: To develop a system capable of accurately predicting and managing passenger flow at TSA checkpoints, thereby reducing wait times and improving queue management.

- Optimize Resource Allocation: To utilize the Digital Twin model for effective resource allocation, ensuring TSA staff and equipment are utilized in the most efficient manner.

- Improve Passenger Experience: To enhance the overall experience of travelers by reducing delays and streamlining the security process, thereby contributing to increased passenger satisfaction.

- Maintain High Security Standards: To ensure that any improvements in efficiency do not compromise the stringent security measures necessary at airport checkpoints.

- Incorporate Advanced Technologies: To integrate cutting-edge technologies such as Google's PaLM 2 LLM and Open AI's GPT 4 to automate and refine the operations management models and improve user interaction with the Digital Twin system.

- Develop a Scalable and Adaptable Model: To create a flexible model that can be adapted to different airport environments and scaled up or down according to specific needs and capacities.

- Pave the Way for Future Research and Applications: To establish a foundation for further research in the application of Digital Twin technology in airport operations and other areas of transportation security and management.

## Project Challenges

During the development of the full-scale Digital Twin model for enhancing TSA operations, the project team faced and overcame numerous challenges, particularly in the post-Phase 1 phase of the project. These challenges were critical in refining the model to more accurately reflect real-world conditions and in effectively harnessing the PaLM Suite for the project's needs.

- Optimization Module Enhancement: Integrating nonlinearity into the objective function required verification of the convexity of the queuing theory function. This was essential as the effectiveness of the optimization module relied on a convex objective function for valid minimization​​.

- Differentiating Between Global and Local Minima: A significant challenge was to differentiate between global and local minima, especially during iterations of the Gradient Descent Algorithm. This required strategic selection of initial values for decision variables to bypass local minima​​.

- Scale of Feasible Solutions: Managing the scale of feasible solutions was substantial, with 40 binary decision variables leading to over a trillion possible values. This necessitated considerable computational resources and the introduction of additional constraints specific to the domain​​.

- Incorporating Multiple Parameters into Queuing Theory: Incorporating multiple parameters into the queuing theory added complexity, necessitating changes to nearly all formulas. This allowed the creation of a unified model applicable to both supply-constrained and demand-constrained scenarios​​.

- Challenges with PaLM Suite in Codifying Operations Management Formulae: The team faced difficulties in ensuring that the PaLM Suite could reliably produce correct estimates. This involved numerous iterations and adjustments to address issues like PaLM misinterpreting formulas, yielding inaccurate numerical results, and difficulty in establishing connections between different solution sections​​.

- Prompt Size Restrictions and Model's Learning Potential: The stringent character count limit during training posed a challenge, especially for intricate tasks. This led to a truncated learning experience, forcing the team to condense prompts and omit certain contextual details to make effective use of the character allowance​​.

- Temperature Settings and Reversion to Model’s Baselines for Token Prediction: The pre-existing knowledge base of the LLM sometimes overrode unique processes being implemented, complicating training. This was attributed to the generally trained corpus of the LLM, resulting in a greater weight on adjacent concepts not entirely relevant to the specific situation​​.

- Human-Computer Interaction (HCI) Framework Limitations: The LLM's inadequate execution of arithmetic operations and the character count limit led to a dilution of context and a degradation in the granularity of data translation. This demanded increased cognitive effort from users, highlighting flaws within the HCI framework and the need for more intuitive and less burdensome interactions​​.

These challenges not only tested the team's problem-solving skills but also contributed to the advancement of the project, enhancing its efficiency and applicability to TSA operations.


## Implementation

The development of the Digital Twin model for enhancing TSA operations involved several key phases, each utilizing specific tools and methodologies:

### Phase 1: Base Model Conceptualization and Initial Prototyping

**Tool Used**: Microsoft Excel
**Objective**: To demonstrate the viability of the project and the potential of the envisioned model, two base models were developed in Microsoft Excel. These models formed the foundation for the more comprehensive model that was to be developed later​​.


### Phase 2: Advanced Model Development and Integration

**Challenges**: This phase involved refining the baseline implementation from Phase 1. Key challenges included integrating nonlinearity into the objective function, verifying the convexity of the queuing theory function, differentiating between global and local minima, managing the scale of feasible solutions, and incorporating multiple parameters into the queuing theory. These challenges were critical in enhancing the optimization module to more accurately reflect real-world conditions​​.


### Phase 3: Model Conversion to Machine-Readable Format via MakerSuite

**Tools Used**: Excel, Python, MakerSuite
**Objective**: The aim was to codify existing Operations Management models into machine-readable instructions and develop a platform for end-users of the Digital Twin to make informed decisions about the underlying queue management process. This phase combined the robust data structuring of Excel with the advanced computational abilities of Python and the linguistic proficiency of PALM’s LLM​​.


### Phase 4: Overall Project Integration via Python and GPT 4

**Tools Used**: Excel, Python, ChatGPT
**Objective**:The fusion of these use cases and tools enhanced the practicality of the existing Digital Twin project. The ultimate goal was to create a system that was not only functional but also user-friendly and intuitive, minimizing the need for specialized skills or domain knowledge from users, particularly TSA agents​​.

This multi-phase approach, leveraging various tools and overcoming specific challenges, was integral to the successful development of the Digital Twin model aimed at improving TSA checkpoint efficiency.


## Contributing to the Project

We welcome contributions from the community to further enhance and expand the capabilities of the Digital Twin model for enhancing airport security checkpoint efficiency. Whether you're a researcher, developer, TSA professional, or simply interested in contributing to the project, here are ways you can get involved:

- **Providing Feedback and Suggestions**: Share your insights, experiences, and suggestions for improvements. Feedback from TSA personnel, airport staff, and passengers can provide valuable perspectives that help refine the model's effectiveness and usability.

- **Collaborating on Research and Development**: Researchers and developers are encouraged to collaborate on advancing the model's technology, integrating new features, or adapting it for different environments such as amusement parks or other capacity studies.

- **Testing and Validation**: Assistance in testing the model in various scenarios, and providing data for validation purposes can significantly improve its accuracy and reliability.

- **Sharing Data and Case Studies**: Contributing anonymized data sets or case studies related to TSA operations or crowd management in different settings can help in refining the model's predictive algorithms and expanding its applicability.

- **Documentation and Educational Materials**: Contributing to the development of comprehensive documentation, tutorials, and educational materials can make the model more accessible to a wider audience, including those without specialized technical knowledge.

- **Community Engagement and Awareness**: Helping to raise awareness about the project through community engagement, presentations, and publications can attract more contributors and users, fostering a collaborative ecosystem.

- **Financial Support or Sponsorship**: Financial contributions or sponsorships can support ongoing research, development, and implementation efforts, ensuring the continuous improvement of the project.

- **Code Contributions**: For those with technical expertise, contributing code, bug fixes, and feature enhancements through platforms like GitHub can directly impact the project's development.

To contribute, please reach out through our project's contact channels. We are committed to fostering an inclusive and collaborative environment where diverse ideas and contributions are valued and respected. Together, we can drive innovation and make a meaningful impact in enhancing airport security and efficiency.



## Contact Information
Email: Raymondpeterdavid@gmail.com

