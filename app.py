from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import StreamingResponse
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import os
from datetime import datetime
from docx2pdf import convert
import tempfile
from typing import Optional
from pydantic import BaseModel
import io
import base64

app = FastAPI()

class RentBillData(BaseModel):
    month: str
    owner_name: str
    owner_aadhar: str
    owner_acc: str
    renter_name: str
    sr_no: str
    date: str
    mobile: str
    monthly_rent: str
    increment: str
    total_after_increment: str
    tds_amount: str
    amount_paid: str
    image_base64: Optional[str] = None

def generate_rent_bill(data: RentBillData):
    try:
        # Check if template exists
        if not os.path.exists("template.docx"):
            raise FileNotFoundError("Template file 'template.docx' not found")

        # Create temporary directory for files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Load the DOCX template
            doc = DocxTemplate("template.docx")

            # Variables to replace
            context = {
                "month": data.month,
                "owner_name": data.owner_name,
                "owner_aadhar": data.owner_aadhar,
                "owner_acc": data.owner_acc,
                "renter_name": data.renter_name,
                "sr_no": data.sr_no,
                "date": data.date,
                "mobile": data.mobile,
                "monthly_rent": data.monthly_rent,
                "increment": data.increment,
                "total_after_increment": data.total_after_increment,
                "tds_amount": data.tds_amount,
                "amount_paid": data.amount_paid
            }

            # Handle image if provided
            if data.image_base64:
                try:
                    # Decode base64 image
                    image_data = base64.b64decode(data.image_base64)
                    
                    # Save image to temporary file
                    image_path = os.path.join(temp_dir, "temp_image.png")
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_data)
                    
                    # Create InlineImage object with proper size
                    image = InlineImage(doc, image_path, width=Mm(30))  # 30mm width
                    context["image"] = image
                except Exception as e:
                    raise ValueError(f"Failed to process image: {str(e)}")

            # Generate unique filenames in temp directory
            output_docx = os.path.join(temp_dir, "rent_bill.docx")
            output_pdf = os.path.join(temp_dir, "rent_bill.pdf")

            # Replace variables and save DOCX file
            doc.render(context)
            doc.save(output_docx)

            # Convert DOCX to PDF using docx2pdf
            try:
                convert(output_docx, output_pdf)
            except Exception as e:
                raise RuntimeError(f"Failed to convert DOCX to PDF: {str(e)}")

            if not os.path.exists(output_pdf):
                raise FileNotFoundError(f"PDF file was not generated: {output_pdf}")

            # Read the PDF file into memory
            with open(output_pdf, "rb") as f:
                pdf_content = f.read()

            return pdf_content

    except Exception as e:
        raise e

@app.post("/generate-bill")
async def generate_bill(data: RentBillData):
    try:
        # Generate the bill and get the PDF content
        pdf_content = generate_rent_bill(data)

        # Return the file as a streaming response
        return StreamingResponse(
            io.BytesIO(pdf_content),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=rent_bill.pdf"}
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 