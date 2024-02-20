# Project Name README

## API Reference

### Authentication
- **Login**: 
  - Endpoint: `account/login/`
  - Method: POST
  - Description: Authenticates user and provides access and refresh tokens.

  - Body

  ```json
  {
    "email":"email",
    "password":"pass@123"
  }
  ```

- **User Registration**: 
  - Endpoint: `account/register/`
  - Method: POST
  - Description: Registers a new user.

  - Body

  ```json
  {
    "email":"email",
    "password":"pass@123",
    "role":"customer",
    "mobile_no":121212212,
    "name":"john doe"
  }
  ```

### User Management
- **User Profile**: 
  - Endpoint: `account/`
  - Method: GET
  - Description: Retrieves user profile details.
  - Auth token required

- **Verify OTP**: 
  - Endpoint: `account/verify/`
  - Method: POST
  - Description: Verifies user's email with OTP.

  - Body

  ```json
  {
    "email":"email",
    "otp":1234
  }
  ```

- **Forgot Password**: 
  - Endpoint: `account/forget-password/`
  - Method: POST
  - Description: Sends a password reset link to the user's email.

  - Body

  ```json
  {
    "email":"email"
  }
  ```

- **Reset Password**: 
  - Endpoint: `account/reset-password/<str:uidb64>/<str:token>/`
  - Method: POST
  - Description: Resets user's password using a valid token.

  - Body

  ```json
  {
    "new_password":"pass@123"
  }
  ```

- **Edit Profile**: 
  - Endpoint: `account/edit-profile/`
  - Method: GET (to retrieve), PATCH (to update)
  - Description: Retrieves or updates user profile details.

  

- **Role**:
  - Endpoint: 

### Address Management
- **User Addresses**: 
  - Endpoint: `account/user-address/`
  - Method: GET, POST
  - Description: Retrieves user's addresses or adds a new address.
- **Update Address**: 
  - Endpoint: `account/user-address/<int:pk>/`
  - Method: PATCH, PUT, DELETE
  - Description: Updates, deletes or sets as active a specific address.

### Policy Management
- **Privacy Policy**: 
  - Endpoint: `static_data/privacy-policy/`
  - Method: GET
  - Description: Retrieves the privacy policy.

- **Refund and Cancellation Policy**: 
  - Endpoint: `static_data/refund-cancellation-policy/`
  - Method: GET
  - Description: Retrieves the refund and cancellation policy.

- **Terms and Conditions**: 
  - Endpoint: `static_data/terms-and-condition/`
  - Method: GET
  - Description: Retrieves the terms and conditions.


- **Sample Product Request**
  - Endpoint: `product/`
  - Method: GET,POST
  - Description: Retrive and Add Product.

  Sample Body

  ```json
    {
    "product_name": "Sample Product",
    "description": "This is a sample product description.",
    "image": "base64_encoded_image_here",
    "stock_quantity": 10,
    "main_category": 1,
    "sub_category": 1,
    "sku_code": "ABC123",
    "disable": false,
    "size_charts": [
      {
        "size": "Small",
        "quantity": 20,
        "finish": 1, 
        "role_prices": [
          {
            "role": 1,  
            "price": 10.99,
            "price_with_gst": 12.99
          },
          {
            "role": 2,
            "price": 12.99,
            "price_with_gst": 15.99
          }
        ]
      },
      {
        "size": "Medium",
        "quantity": 15,
        "finish": 2,
        "role_prices": [
          {
            "role": 1,
            "price": 15.99,
            "price_with_gst": 18.99
          },
          {
            "role": 2,
            "price": 18.99,
            "price_with_gst": 21.99
          }
        ]
      }
    ],
    "images": [
      {
        "image": "base64_encoded_image_data_here" 
      },
      {
        "image": "base64_encoded_image_data_here"
      }
    ],
    "locations": [
      {
        "godown_number": "A1",
        "room_number": "101",
        "rack_number": "B2"
      },
      {
        "godown_number": "B2",
        "room_number": "202",
        "rack_number": "C3"
      }
    ]
  }
```