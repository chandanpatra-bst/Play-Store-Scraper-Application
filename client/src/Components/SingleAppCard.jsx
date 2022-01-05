import React from "react";
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import Rating from '@mui/material/Rating';
import './SingleAppCard.css';

function SingleAppCard(props) {
     
    const appUrl = "/appdetails/id=" + props.id
    var app_star_count = parseInt(props.app_star_count)

    return (
        <div className="app-card-container">
            <div className="icon-container">
                <img crossorigin="anonymous" src={props.icon_url} />
            </div>
            <div className="app-info-container">
                <div className="app-title">
                    {props.title}
                </div>
                <div className="app-developer">
                    {props.developer}
                </div>
                <div className="app-star-div">
                    <Rating name="half-rating" value={app_star_count} precision={0.5} />
                </div>
                <a className="app-details-anchor" href={appUrl} target="_blank" rel="noreferrer noopener">
                    <ArrowForwardIosIcon fontSize="small"/>
                </a>
            </div>
        </div>
    )
}

export default SingleAppCard;