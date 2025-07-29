1. Introduction
AgroTrade is a P2P on-chain marketplace that helps farmers and cooperatives sell their produce directly to consumers and enables the exchange of agricultural byproducts between consumers, farmers, and agribusinesses.

2. 2. Requirements
Core Features:
User Authentication: Secure sign-up and login using email, phone, or social media accounts.
Account type: Home/Consumer, Farmer, Agribusiness
Role dashboard display based on account type
	User - Consumer
Marketplace 
Cards to view product pictures, details, and price.
Order requests are sent to notifications page, as well as interactions involved - depending on the interaction, invoices are generated and you proceed to chat UI to finalize trx and checkout
Section for filters - Location, price, quantity.
Cart Icon at the top of the page to reflect that item has been added to cart
Cart Page
Pay here
Invoice for all products added to cart - Farmers end
Total amount generated for all products - Total
Checkout Process
Redirect to payment gateway
Post Payment
Payment is held in escrow
*** Upon delivery - Consumer is required to perform an action to release funds to farmers on time.
User - Farmer  
Listings Page
Farmer can view all product ever listed 
Edit and Delete buttons on each product listing displayed
Top corner button “Create New Listing”
Upload Image button
Input fields for - Name of product, description, Price, “Next” Button
Dashboard
Welcome message - Format: Welcome + “Farmer's name”
Cards at the top of the screen, displaying (in figures)
All listings
Total product sold
Revenue
Requests
Recent Listing section
Notifications page
Receives order requests from farmers



Agrotrade
- [ ] Authentication
    - [ ] User roles (super admin, admin, farmer, customer)
    - [ ] Sign in
    - [ ] Sign up
- [ ] Products
    - [ ] Farmer
        - [ ] List products (and maintain, CRUD)
    - [ ] Customer
        - [ ] View product listings by location
        - [ ] Filter listing
        - [ ] Place order
- [ ] Order
    - [ ] Farmer
        - [ ] View Active/Pending Orders
        - [ ] Change status (accept_reject_order)
        - [ ] Initiate Chat with Customer
    - [ ] Customer
        - [ ] Place Order
        - [ ] View Active/Pending Orders
        - [ ] Change status (paid, collected, report)
        - [ ] Initiate Chat with Farmer
- [ ] Profile Management
    - [ ] Update name