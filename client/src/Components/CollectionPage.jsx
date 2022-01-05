import React, { useState, useEffect } from "react";
import CollectionAppsComponent from "./CollectionAppsComponent";
import ReplayIcon from '@mui/icons-material/Replay';
import './CollectionPage.css';
import configData from "../config.json";

function CollectionPage() {
    
    const [data, setData] = useState({})
    const URL = configData.BACKEND_SERVER_URL;
    
    useEffect(() => {
        fetch(URL).then(
            res => res.json()
        ).then(
            data => {
                setData(data)
            }
        )
    }, [])

    function handleClick() {
        fetch(URL + "/scrape").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
            }
        )
    }


    return (
        <div className="top-container">
            <div className="top-charts-container">
                <h1 className="top-charts-heading">Top Charts</h1>
            </div>
            <div className="rescrape-container">
                <button className="btn" onClick={handleClick}>
                    <ReplayIcon />
                </button>
            </div>
            {
                Object.keys(data).map((key, index) => {
                    return (
                        <CollectionAppsComponent title={key} appsData={data[key]} key={index}/>
                    )
                })
            }
        </div>
        
    )

}

export default CollectionPage;