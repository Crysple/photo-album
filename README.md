# Introduction
This is a serverless photo album web application, that can be searched using natural language through both text and voice. The architecture diagram is as follow:

![image](https://user-images.githubusercontent.com/20517842/81481568-2748ec80-91ff-11ea-8ab4-d4d73bd18b2a.png)


- **B1** is a **S3 bucket** stores front-end stuff, together with **API Gateway**, **LF2** (Lambda Function 2) forming a website that can handle user request (upload photo, search photo by text, search photo by voice, etc.)
- A new photo is uploaded to another **S3 bucket** **B2**, which that trigger **LF1** to parse the photo using **AWS Rekognition** that returns some keywords of the photo. Then **LF1** stores the keywords with storage information of the photo in the **ElasticSearch** for furture indexing.
- When user types in a sentence like "show me my cats", it is handled by **LF2**, which further utilize **Lex** to parse the sentence and get the keyword ('cats' in this case), then return the corresponding photos that contains that keyword.


# Usage

A **cloudformation template yaml file** is in the root directory, which automatically builds up all the necessary Amazon Web Services, including **two pipelines** that help automatic code update from github and **continuous delivery**.

- LFPipeline: Build two lambda functions and the S3 storing photos (there's a trigger so I put them together for convenience). Plus, api gateway is also built here.
- PipelineS3: This is for the front-end code. Note that **the front-end code is in the `front-end` branch**
- Elastic Search

Note that there's no template for Lex so it should be built manually.