import requests
import os
from datetime import datetime
import json
from typing import Optional
import base64

def encode_image_to_base64(image_path: str) -> Optional[str]:
    """Encode an image file to base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ Error encoding image: {str(e)}")
        return None

def test_generate_bill(image_path: Optional[str] = None):
    # API endpoint
    url = "http://localhost:8000/generate-bill"
    
    # Bill data
    bill_data = {
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
    
    # Add image if provided
    if image_path:
        print(f"🖼️ Processing image: {image_path}")
        image_base64 = encode_image_to_base64(image_path)
        if image_base64:
            bill_data["image_base64"] = image_base64
            print("✅ Image successfully encoded to base64")
        else:
            print("⚠️ Proceeding without image")
    
    try:
        print("🚀 Testing Rent Bill Generator API...")
        print("📝 Request data:")
        # Don't print the full base64 string if present
        print_data = bill_data.copy()
        if "image_base64" in print_data:
            print_data["image_base64"] = f"[Base64 image data: {len(print_data['image_base64'])} bytes]"
        print(json.dumps(print_data, indent=2))
        
        # Make POST request to the API with the bill data
        response = requests.post(url, json=bill_data)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Check if the response is a PDF file
            if response.headers.get('content-type') == 'application/pdf':
                # Generate a unique filename for the downloaded PDF
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"downloaded_bill_{timestamp}.pdf"
                
                # Save the PDF file
                with open(output_file, "wb") as f:
                    f.write(response.content)
                
                # Get file size in KB
                file_size = os.path.getsize(output_file) / 1024
                
                print("\n✅ Bill generated successfully!")
                print(f"📄 PDF saved as: {output_file}")
                print(f"📂 File size: {file_size:.2f} KB")
                print(f"🔗 Content-Type: {response.headers.get('content-type')}")
                print(f"📦 Content-Length: {len(response.content)} bytes")
            else:
                print("\n❌ Error: Response is not a PDF file")
                print(f"Content-Type: {response.headers.get('content-type')}")
                print("Response content:")
                print(response.text)
        else:
            print("\n❌ Error: Request failed")
            print(f"Status Code: {response.status_code}")
            print("Response content:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server")
        print("Please make sure the FastAPI application is running")
        print("You can start it with: python app.py")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {str(e)}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Test the Rent Bill Generator API')
    parser.add_argument('--image', type=str, help='Path to the image file to include in the bill')
    args = parser.parse_args()
    
    test_generate_bill(args.image) 