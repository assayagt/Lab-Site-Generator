import React from "react";
import "./HomePage.css";
import AboutUs from "../../Components/AboutUs/AboutUs";
import { useAuth } from "../../Context/AuthContext";


function HomePage(props) {
  
  const { fetchToken } = useAuth();
  function fetchData() {
    const storedSid = sessionStorage.getItem('sid');
    if (!storedSid) {
      fetchToken();  
    }    
  }

  return (
      <div className='HomePage'>
          {fetchData()}
        <div className="main_section_homePage">
            <div className="subTitle">Welcome to our lab website.</div>
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