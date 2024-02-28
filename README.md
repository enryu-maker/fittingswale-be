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

- **Main Categories Request**
  - Endpoint: `product/main-categories/`
  - Method: GET,POST
  - Description: Retrive Main Categories Only.

- **Sub Categories Request**
  - Endpoint: `product/sub-categories/`
  - Method: GET,POST
  - Description: Retrive Sub Categories Only.

- **Main with Sub Categories Request**
  - Endpoint: `product/main-category-with-sub/`
  - Method: GET,POST
  - Description: Retrive Main Categories with Sub Category.

- **Sub Categories with Products Request**
  - Endpoint: `product/sub-category-with-prod/<int:id>/`
  - Method: GET,POST
  - Description: Retrive Sub Categories with Products.

- **Payment Gateway**
  - Endpoint: `product/paymenttransactions/`
  - Method: POST
  - Description: Order Payment Gateway
  - Body
  
  ```json
  {
    "currency": "INR",
    "payment_method": "cod",
    "payment_date": "2024-02-29T12:00:00",
    "items": "items list",
    "subtotal": "sub total dict",
    "subtotal_qty": "sub qty dict",
    "address": "address dict",
    "total": "30.00"
}
  ```