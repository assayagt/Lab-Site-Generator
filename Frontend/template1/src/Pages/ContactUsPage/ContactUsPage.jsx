import React from "react";


function ContactUsPage(props) {
  return(
    <div>
        <div>Contact Us</div>
        <div>{props.address}</div>
        <div>{props.email}</div>
        <div>{props.phone}</div>
    </div>
  )
}

export default ContactUsPage;