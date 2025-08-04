# 🌩️ Cloud Immunity System – AWS Resource Tracker & Auto-Cleanup

> A serverless, secure, and cost-effective AWS automation tool to **scan**, **report**, and **clean up** unused cloud resources.

---

## 📌 Project Overview

The **Cloud Immunity System** is designed to help AWS users reduce cloud bills and improve infrastructure hygiene by identifying and optionally removing unused or idle AWS resources such as:

- EC2 Instances
- EBS Volumes
- S3 Buckets
- RDS Instances
- Lambda Functions
- Elastic IPs

It sends **daily or weekly email reports** listing all unused resources with actionable "Stop" and "Delete" buttons — all while maintaining **secure access control** through **API Gateway**, **password validation**, and **API keys**.

---

## 🎯 Problem Statement

Many organizations leave behind unused or idle AWS resources that continue to:
- Incur unnecessary **costs**
- Create **clutter**
- Reduce **resource visibility**
- Increase **management overhead**

Manually tracking and deleting these is error-prone and time-consuming. This project automates the entire process using native AWS services.

---

## ✅ Features

- 🔍 **Detects Idle Resources**: EC2, EBS, S3, RDS, Lambda, and Elastic IPs
- 📬 **Sends Email Alerts**: Daily/Weekly HTML reports via Amazon SES
- 🔐 **Secure Cleanup**: API Gateway + password-protected delete UI
- 🧠 **Tag-Aware**: Extracts owner details from resource tags
- 🧼 **Auto or Manual Cleanup**: Supports both approaches
- ☁️ **100% Serverless**: No EC2 needed — powered by AWS Lambda
- 🔧 **Customizable**: Region, thresholds, recipients, and tagging rules

---

## 🔧 Architecture
EventBridge (Scheduler)
|
v
[ Lambda 1: Scanner ] ─────→ [ Amazon SES Email ]
|
v
[ API Gateway ] ←────── "Stop" / "Delete" Links
|
v
[ Lambda 2: Password Validator ]
|
v

[ Lambda 3: Resource Action (Stop/Delete) ]

---

## 🛠️ Technologies & Services Used

| Category         | Tools / Services                                |
|------------------|--------------------------------------------------|
| Cloud Platform   | AWS                                              |
| Programming Lang | Python 3.x                                       |
| SDK              | Boto3 (AWS SDK for Python)                       |
| Services Used    | Lambda, SES, EC2, RDS, S3, EventBridge, API Gateway, IAM |
| Deployment Tool  | AWS Console / SAM CLI / GitHub Actions (optional) |
| Email Reports    | Amazon SES (Verified Email Required)            |

---

## 🧩 Lambda Function Breakdown

| Function Name        | Role                                            |
|----------------------|--------------------------------------------------|
| **ScannerFunction**  | Scans for unused resources, sends email via SES |
| **PasswordValidator**| Displays password input UI for delete security  |
| **DeleteHandler**    | Deletes a resource after password verification  |
| **StopHandler**      | Stops/Disables resource (optional)              |

---

## 🔐 Security Measures

- ✅ **API Gateway**: Restricts unauthorized access using **API Keys**
- 🔑 **Password Validation**: Prevents accidental deletion of live resources
- 📜 **IAM Roles**: Follow least privilege for Lambda execution
- 🔍 **CloudWatch Logs**: Logs all actions for audit and debugging
- 🔒 **HTTPS Endpoints**: All interactions are encrypted

---

## 📁 Project Structure
cloud-immunity-system/
│
├── scanner_function.py # Lambda 1 - Scanning and reporting
├── password_validator.py # Lambda 2 - Password check
├── delete_handler.py # Lambda 3 - Deletion logic
├── stop_handler.py # Optional stop handler
├── config.json # Configuration file
├── requirements.md # Dependencies & tools
└── README.md



---

## ⚙️ Requirements

- ✅ AWS Account with IAM Access
- ✅ Amazon SES Verified Sender Email
- ✅ AWS Region: `us-east-1` (can be changed in config)
- ✅ IAM Role with permissions: `ec2:*`, `s3:*`, `rds:*`, `lambda:*`, `ses:SendEmail`, `logs:*`, `cloudwatch:*`, `iam:PassRole`
- ✅ Python 3.8+ and `boto3` installed (for local testing)

---

## 🧪 Testing the System

1. 📨 **Check SES Verification**  
   Verify sender/receiver email addresses in SES sandbox mode.

2. 🧪 **Manually Trigger Lambda 1**  
   Upload test resources and run the scanner function.

3. 🔗 **Click Action Links from Email**  
   Use a browser or Postman to test the Stop/Delete links.

4. 🔐 **Enter Password**  
   Try incorrect password first → see error handling  
   Try correct password → resource gets deleted/stopped

---

## 📬 Sample Email Preview

```html
Cloud Immunity System Daily Report

| Resource Type | Resource ID | Status | Owner | Actions     |
|---------------|-------------|--------|-------|-------------|
| EC2 Instance  | i-0abc123...| inactive | DevOps | [Stop] [Delete] |
| S3 Bucket     | logs-only-bucket | inactive | Analytics | [Delete] |

Click links above to manage your cloud cost and cleanup idle resources.

Email Dashboard :
![WhatsApp Image 2025-08-02 at 12 17 29_6b6fcef7](https://github.com/user-attachments/assets/758da94d-6e5b-4f70-9913-e20ea466df3e)

Stop Password Verification : 
![WhatsApp Image 2025-08-02 at 12 17 48_4c0d900d](https://github.com/user-attachments/assets/cf6c52d2-b48a-4105-8a40-c4c79e868ffc)

Delete Password Verification :
![WhatsApp Image 2025-08-02 at 12 18 08_0e4b1098](https://github.com/user-attachments/assets/c9f10eab-3258-45a9-940f-f4d7be33345a)
