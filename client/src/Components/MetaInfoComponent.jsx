import React from "react";
import './MetaInfoComponent.css';

function MetaInfoComponent(props) {
    
    return (
        <div className="meta-container">
            <strong>{props.infoTitle}</strong>
            <p>{props.info}</p>
        </div>
    )
}

export default MetaInfoComponent;