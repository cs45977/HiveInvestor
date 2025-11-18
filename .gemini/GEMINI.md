#GEMINI.md - context file

#Included Context Files

@./Test_Driven_Instructions.MD

@./APP_Design_Instructions.md

@../Application_description.md

@./context/Deployment.md 

@./context/LocalDevGuide.md 

@./context/DevelopmentPlan.md 

@./context/TechnicalDesign.md 

@./context/VisualDesign/styleguide.pdf 

#@./context/testing/* 

#@./VisualDesign/*

#If included files can not be loaded, inform me of which files are missing before executing any prompts

#application description
- The application description is found in the Application_description.md


#Instructions
- My preferred development framework is python FastAPI with a VUE.js frontend and tailwinds.css 
- We will deploy our application to Google Cloud Platform
- Local development should utilize virtual machines on VirtualBox
- The local development guide is used to instruct developers how to configure their local systems for development of the system 
- The local development Guide should include links to all needed resources & instructions for initial configuration of the environment
- My local development host is a Macbook
- Technical Design Docs are defined in App_Design_Instructions.md 
- If the technical design document (./context/TechnicalDesign.md) has not been created, use the Application_Description.md to provide the context to create it in the context/ directory. 
- If the Development plan document (./context/DevelopmentPlan.md) has not been created, create it in the context/ directory.
- If the deployment guide (./context/Deployment.md) has not been created, guide me through creating it. 
- The deployment guide is used to instruct developers or SRE on the process for deploying their code to GCP 
- If the Developer's Local Environment Guide (./context/LocalDevGuide.md) has not been created, guide me through creating it. 
- Within the development plan, all stories need to indicate their status 'Not Started', 'In Progress', 'Blocked', or 'Complete'. 
- When a Development plan story item is worked on the status must be updated in the DevelopmentPne document 
- If FrontEndTestPlan.md or BackEndTestPlan.md do not exist, create testing plan documents that provides instructions for testing backend and frontend stories. 
- When a Story is completed, the testing plan document must be updated to provide instructions for testing that story. 
- The testing plans should be located at ./context/testing/FrontEndTestPlan.md for front end testing and ./context/testing/BackEndTestPlan.md for backend tests
- Do not offer to start any local servers for me .  I will manually start, stop , or restart any servers
- Do not offer to take any git actions for me.  I will manually add, commit, and push to git 
- All files in the context directory need to be served in a web ui so that teams can review them in their browser 
- We will deploy our application to Google Cloud Platform
- When creating a development plan create an epic 0 which allows for the creation of a "Hello world" app and its deployment.  The hello world app should be used that we can deploy and test our application both localy and to GCP                

