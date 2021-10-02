import { Route, Redirect} from 'react-router-dom'
import React, { Component } from 'react'
import { useSelector } from 'react-redux';


function ProtectedRoute({ component: Component, ...rest }) {

    const isAuth = useSelector(state => state.user.isAuth);

    return (  
        <Route
            {...rest}
            render={(props) => {
                if(isAuth)
                    return <Component />
                else
                    return <Redirect to={{pathname: "/auth", state: {from: props.location}}}/>
            }}
        />
    );

}

export default ProtectedRoute
