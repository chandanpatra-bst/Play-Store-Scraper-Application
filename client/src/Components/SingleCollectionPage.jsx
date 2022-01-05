import React, { useState, useEffect } from "react";
import SingleAppCard from "./SingleAppCard";
import './SingleCollectionPage.css';
import configData from "../config.json";

function SingleCollectionPage(props) {

    var { name } = props.match.params
    const [data, setData] = useState([])
    const url = configData.BACKEND_SERVER_URL + "/collection?name=" + name

    var title = name.split('-').map((part) => {
        return part.charAt(0).toUpperCase() + part.slice(1);
    }).join(' ');

    useEffect(() => {
        fetch(url).then(
            res => res.json()
        ).then(
            data => {
                setData(data)
            }
        )
    }, [])

    return (
        <div className="top-container">
            <div className="title-container">
                <h1 className="title">{ title }</h1>
            </div>
            <div className="apps">
                {
                    Object.keys(data).map((index) => {
                        return (
                            <SingleAppCard 
                                title = {data[index].title}
                                id = {data[index].id}
                                icon_url = {data[index].icon_url}
                                developer = {data[index].developer}
                                app_star_count = {data[index].app_star_count} 
                            />
                        )
                    })
                }
            </div> 
            
        </div>
    )
}

export default SingleCollectionPage;