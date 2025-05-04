# Rent Bill Generator API

A FastAPI application that generates rent bills in PDF format from a DOCX template.

## Features

- Generate rent bills in PDF format
- Dynamic data input through API
- No files stored on server
- Docker support

## Prerequisites

- Docker (for containerized deployment)
- Or Python 3.11+ (for local development)

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t rent-bill-generator .
```

2. Run the container:
```bash
docker run -p 8000:8000 rent-bill-generator
```

## API Usage

Send a POST request to `/generate-bill` with the following JSON body:

```json
{
    "month": "MAY",
    "owner_name": "Sandeep Balkrishna Patil",
    "owner_aadhar": "2376 1617 3534",
    "owner_acc": "020301541637",
    "renter_name": "Sudhir Power Limited",
    "sr_no": "36",
    "date": "02/05/2025",
    "mobile": "7355556255",
    "monthly_rent": "1,32,069",
    "increment": "5% = 6603.45",
    "total_after_increment": "1,38,672.45",
    "tds_amount": "13,867",
    "amount_paid": "1,24,805"
}
```

The API will return a PDF file with the generated rent bill.

## Required Files

- `template.docx`: The DOCX template file for the rent bill
- `app.py`: The FastAPI application
- `requirements.txt`: Python dependencies
- `Dockerfile`: For containerization 