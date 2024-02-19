# Project Name README

## API Reference

### Authentication
- **Login**: 
  - Endpoint: `account/login/`
  - Method: POST
  - Description: Authenticates user and provides access and refresh tokens.

- **User Registration**: 
  - Endpoint: `account/register/`
  - Method: POST
  - Description: Registers a new user.

### User Management
- **User Profile**: 
  - Endpoint: `account/`
  - Method: GET
  - Description: Retrieves user profile details.

- **Verify OTP**: 
  - Endpoint: `account/verify/`
  - Method: POST
  - Description: Verifies user's email with OTP.

- **Forgot Password**: 
  - Endpoint: `account/forget-password/`
  - Method: POST
  - Description: Sends a password reset link to the user's email.

- **Reset Password**: 
  - Endpoint: `account/reset-password/<str:uidb64>/<str:token>/`
  - Method: POST
  - Description: Resets user's password using a valid token.

- **Edit Profile**: 
  - Endpoint: `account/edit-profile/`
  - Method: GET (to retrieve), PATCH (to update)
  - Description: Retrieves or updates user profile details.

### Address Management
- **User Addresses**: 
  - Endpoint: `/user-address/`
  - Method: GET, POST
  - Description: Retrieves user's addresses or adds a new address.
- **Update Address**: 
  - Endpoint: `/user-address/<int:pk>/`
  - Method: PATCH, PUT, DELETE
  - Description: Updates, deletes or sets as active a specific address.

### Policy Management
- **Privacy Policy**: 
  - Endpoint: `/privacy-policy/`
  - Method: GET
  - Description: Retrieves the privacy policy.

- **Refund and Cancellation Policy**: 
  - Endpoint: `/refund-cancellation-policy/`
  - Method: GET
  - Description: Retrieves the refund and cancellation policy.

- **Terms and Conditions**: 
  - Endpoint: `/terms-and-condition/`
  - Method: GET
  - Description: Retrieves the terms and conditions.


