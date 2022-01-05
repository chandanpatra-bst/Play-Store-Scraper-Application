import React, { useState, useEffect } from "react";
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp';
import MetaInfoComponent from './MetaInfoComponent';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import DeveloperComponent from './DeveloperComponent';
import ArrowBackIosNew from "@mui/icons-material/ArrowBackIosNew";
import ReactPlayer from "react-player";
import { ClapSpinner } from "react-spinners-kit";
import Carousel from 'react-elastic-carousel';
import './SingleAppPage.css';
import './MetaInfoComponent.css';
import Rating from '@mui/material/Rating';
import configData from "../config.json";


function SingleAppPage(props) {

    const { pkg_id } = props.match.params
  
    const [data, setData] = useState({})
    const [isLoading, setLoading] = useState(true)
    const [isToggleOn, setToggle] = useState(false)

    const url = configData.BACKEND_SERVER_URL + "/appdetails?id=" + pkg_id

    useEffect(() => {
        fetch(url).then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                setLoading(false)
            }
        )
    }, [])
    
    if(isLoading){
        return (
            <div className="Loader">
                <ClapSpinner 
                    size={30}
                    color="#686769" 
                />
                <h2>Loading...</h2>
            </div>
        )
    }
    
    var app_star_count = parseInt(data.app_star_count)
    // var precision = parseInt(data.app_star_count[2])/10

    var screenshotsList = data.screenshots
    
    var description = data.description.slice(0, 500)
    var complete_description = data.description

    return(
        <div className="top-container">
            <div className="upper-container">
                <div className="icon-container">
                    <img crossorigin="anonymous" className="icon" src={data.icon_url} />
                </div>
                <div className="app-info-container">  

                    <div className="heading-container"> 
                        <h1 className="heading">  
                            <span>{data.title}</span>
                        </h1>    
                    </div>
                    <div className="dev-category-container">
                        <span className="dev-cat">{data.developer_id}</span>
                        <span className="dev-cat">{data.category}</span>
                    </div>
                    
                    <div className="app-star-div">
                        <Rating name="half-rating" value={app_star_count} precision={0.5} />
                    </div>

                    <div>
                        <a className="installBtn" href={data.playstore_url} target="_blank" rel="noreferrer noopener"><strong className="install">INSTALL</strong></a>
                    </div>
                </div>
            </div>
        
            <div className="screenshot-video-container">
                {
                    data.video_trailer_url && <ReactPlayer width="320px" height="240px" url={data.video_trailer_url}/>
                }
                <div className="screenshots-container"> 
                    <Carousel itemsToShow={3}>
                        {
                            screenshotsList.map((ss, index) => {
                                return (
                                    <div className="screenshot-div">
                                        <img crossorigin="anonymous" className="screenshot-img" src={ss}/>
                                    </div>
                                )
                            })
                        }
                    </Carousel>
                </div>
            </div>

            <button className="btnContainer" onClick={() => setToggle(!isToggleOn)}>
                {
                    isToggleOn ? (
                        <div className="mid-container">
                            <div className="desc-div">
                                {complete_description}
                            </div>
                            <div className="additional-info-container">

                                <div className="addition-info-heading">
                                    <h3>Additional Information</h3>
                                </div>

                                <div className="meta-info-div">
                                    <MetaInfoComponent 
                                        infoTitle = "Updated"
                                        info = {data.updated_on}
                                    />

                                    <MetaInfoComponent 
                                        infoTitle = "Size"
                                        info = {data.size}
                                    />

                                    <MetaInfoComponent 
                                        infoTitle = "Installs"
                                        info = {data.installs}
                                    />

                                    <MetaInfoComponent 
                                        infoTitle = "Current Version"
                                        info = {data.app_version}
                                    />
                                </div>

                                <div className="meta-info-div">
                                    <MetaInfoComponent 
                                        infoTitle = "Requires Android"
                                        info = {data.requires}
                                    />

                                    <MetaInfoComponent 
                                        infoTitle = "Content Rating"
                                        info = {data.content_rating}
                                    />

                                    <MetaInfoComponent 
                                        infoTitle = "Offered By"
                                        info = {data.offered_by}
                                    />
                                </div>

                                <DeveloperComponent 
                                    dev_website = {data.dev_website}
                                    dev_email = {data.dev_email}
                                    dev_address = {data.dev_address}
                                />
                            </div>
                            <ArrowDropUpIcon />
                        </div>
                    ): (
                        <div className="mid-container">
                            <div className="desc-div">
                                <p>{description}</p>
                                <ArrowDropDownIcon className="arrow-down-button" />
                            </div>
                        </div>
                        
                    ) 
                }   
            </button>
            
        </div>
    )
}

export default SingleAppPage;