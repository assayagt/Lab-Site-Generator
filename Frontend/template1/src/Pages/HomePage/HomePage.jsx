import React from "react";
import "./HomePage.css";
import AboutUs from "../../Components/AboutUs/AboutUs";


function HomePage(props) {


  return (
      <div className='HomePage'>
        <div className="main_section_homePage">
            <div className="subTitle">Welcome to our lab website.<br/> This is where there will be a custom welcome message</div>
            <div className="homeImg">to be img</div>
            {props.about_us?(
                   <AboutUs info={props.about_us}/> ):
                   (<div> </div>
            )
            }
           
        </div>
       
      </div>
    
  );
}

export default HomePage;