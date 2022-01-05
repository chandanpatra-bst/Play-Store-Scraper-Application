import React from "react";
import './DeveloperComponent.css';

function DeveloperComponent(props) {

    return (
        <div className="developer-div">
            <strong>Developer</strong>
            {
                props.dev_website && <p>{props.dev_website}</p>
            }
            {
                props.dev_email && <p>{props.dev_email}</p>
            }
            {
                props.dev_address && <p>{props.dev_address}</p>
            }
        </div>
    )
}

export default DeveloperComponent;