import React, { useState, useEffect } from 'react'
import CollectionPage from './Components/CollectionPage'
import { Switch, Route } from "react-router-dom"
import SingleCollectionPage from './Components/SingleCollectionPage'
import SingleAppPage from './Components/SingleAppPage'

function App() {

    return (

      <>
        <Switch>
          <Route exact path='/'>
            <CollectionPage />
          </Route>
          
          <Route exact path='/collection/:name'
            render={(props) => <SingleCollectionPage {...props} />} 
          />

          <Route exact path='/appdetails/id=:pkg_id'
            render={(props) => <SingleAppPage {...props} />}
          />
          
        </Switch>
      </>
    )

}


export default App;
