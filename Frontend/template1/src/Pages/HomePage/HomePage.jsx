import React from "react";
import "./HomePage.css";
import AboutUs from "../../Components/AboutUs/AboutUs";


function HomePage() {

  const components = [
    "Home",
    "Participants",
    "Contact Us",
    "Publications",
    "About Us"
  ];
  return (
      <div className='HomePage'>
        <div className="main_section_homePage">
            <div className="subTitle">Welcome to our lab website.<br/> This is where there will be a custom welcome message</div>
            <div className="homeImg">to be img</div>
            {components.includes("About Us")?(
                   <AboutUs info="Duis ullamcorper dignissim velit aenean egestas in. Luctus litora imperdiet etiam nascetur turpis nulla ultricies primis. Elementum lacinia sodales neque porta per posuere mus vivamus lacinia. 
                   Imperdiet molestie class maecenas morbi leo sollicitudin risus. 
                   Bibendum etiam vulputate eu sed augue sit at. Vestibulum vehicula a urna massa lobortis sagittis augue suscipit nibh. Vulputate massa mus varius urna id praesent."/> ):
                   (<div> </div>
            )
            }
           
        </div>
       
      </div>
    
  );
}

export default HomePage;