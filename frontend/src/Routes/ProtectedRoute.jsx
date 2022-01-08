import { Route, Redirect } from "react-router-dom";
import React from "react";
import { useSelector } from "react-redux";

function ProtectedRoute({ component: Component, ...rest }) {
  const logged = useSelector((state) => state.auth.logged);

  return (
    <Route
      {...rest}
      render={(props) => {
        if (logged) return <Component />;

        return (
          <Redirect
            to={{ pathname: "/auth", state: { from: props.location } }}
          />
        );
      }}
    />
  );
}

export default ProtectedRoute;
