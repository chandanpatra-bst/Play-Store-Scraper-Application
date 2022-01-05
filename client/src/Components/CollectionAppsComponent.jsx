import React from "react";
import SingleAppCard from "./SingleAppCard";
import './CollectionAppsComponent.css';

function CollectionAppsComponent(props) {
    var collectionName = props.title

    collectionName = collectionName.split(' ').join('-').toLowerCase()
    const browseAllUrl = "/collection/" + collectionName

    const appsDataList = props.appsData

    return (
        <div className="collection-container">
            <div className="collection-browse-container">
                <div className="collection-title-container">
                    { props.title }
                </div>
                <div className="browse-all-container">
                    <button className="btn">
                        <a className="browse-anchor" href={ browseAllUrl } target="_blank" rel="noreferrer noopener">BROWSE ALL GAMES</a>
                    </button>
                </div>
            </div>
            
            <div className="apps-container">
                <SingleAppCard 
                    title = {appsDataList[0].title}
                    id = {appsDataList[0].id}
                    icon_url = {appsDataList[0].icon_url}
                    developer = {appsDataList[0].developer}
                    app_star_count = {appsDataList[0].app_star_count}
                />

                <SingleAppCard
                    title = {appsDataList[1].title}
                    id = {appsDataList[1].id}
                    icon_url = {appsDataList[1].icon_url}
                    developer = {appsDataList[1].developer}
                    app_star_count = {appsDataList[1].app_star_count}
                />

                <SingleAppCard 
                    title = {appsDataList[2].title}
                    id = {appsDataList[2].id}
                    icon_url = {appsDataList[2].icon_url}
                    developer = {appsDataList[2].developer}
                    app_star_count = {appsDataList[2].app_star_count}
                />

                <SingleAppCard 
                    title = {appsDataList[3].title}
                    id = {appsDataList[3].id}
                    icon_url = {appsDataList[3].icon_url}
                    developer = {appsDataList[3].developer}
                    app_star_count = {appsDataList[3].app_star_count}
                />
            </div>

        </div>
    )
}

export default CollectionAppsComponent;