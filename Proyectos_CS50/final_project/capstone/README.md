# LeandroAgristola

# **Real Estate Management Platform**
## **Introduction**
Welcome to my real estate management platform, a web application developed with Django to simplify the management of real estate projects and provide an intuitive user experience. This project combines the best of Django, HTML, CSS, JavaScript, and Bootstrap to create a comprehensive and aesthetically pleasing solution.
## **Key Features**
- **Administration panel**: Allows authorized users to add, edit, and delete real estate developments in a simple and intuitive way.
- **Development catalog**: Displays available real estate projects in an attractive and organized manner.
- **Contact form**: Facilitates communication between interested users and the company.
- **Responsive design**: Ensures an optimal user experience on different devices.
## **Distinction and Complexity**
Our platform stands out for:
- **Advanced customization**: The administration panel allows users to customize each development with images, detailed descriptions, and a Brochure Paper with detailed information about the development.
- **Media integration**: The inclusion of a video player on the homepage enriches the presentation of projects.
- **Efficient data structure**: The Django data model is designed to efficiently manage a large number of real estate developments.
- **User-centered design**: The user interface is intuitive and easy to navigate, improving the end-user experience.
## **Project Architecture**
- **Django**: Provides the foundation for the development of the web application, managing routes, views, and models.
- **HTML, CSS, JavaScript**: Used to create user interfaces and client-side logic.
- **Bootstrap**: CSS framework that facilitates the creation of responsive and attractive designs.
## **How to run the project**
- **Clone the repository**: git clone https://your-repository.git
- **Create a virtual environment**: python -m venv venv
- **Activate the virtual environment**:
    - **Windows**: venv\Scripts\activate
    - **Linux/macOS**: source venv/bin/activate  
- **Install dependencies**: pip install -r requirements.txt
- **Run the development serve**r: python manage.py runserver
- Access http://127.0.0.1:8000/ to view the application.
- Access http://127.0.0.1:8000/management to view the admin section.
    - **User**: admin
    - **Password**: 123456
## **Template Structure**
My application uses a clear and modular template structure to ensure maintainability and code reusability. Templates are located in the templates folder and are divided into the following categories:
## **Base templates**:
- **layout.html**: Defines the general structure of all pages, including the header, footer, and main content section.
- **layout_development.html**: Similar to layout.html, but designed specifically for the pages of the administration panel.
## **Page templates**:
- **home.html**: Contains the main content of the homepage, including the presentation of real estate developments, company information, contact form, and location map.
- **mobileBuildings.html**, **mobiledDwelling.html**, **mobileIndustries.html**: Specialized templates for displaying types of real estate developments on mobile devices, optimizing the view for different screen sizes.
- **login.html**: Displays the login form for the administration panel.
- **management.html**: Lists existing real estate developments, allowing them to be edited and deleted.
- **edit_development.html**, **add_development.html**: Forms for editing and adding new developments, respectively.
## **Benefits of this structure**:
- **Greater maintainability**: By separating the common structure from the variable parts, it facilitates the modification and updating of templates.
- **Reusability**: Inherited blocks allow code sections to be reused in multiple templates.
- **Flexibility**: The modular structure facilitates the creation of new pages and the customization of the application's appearance.
