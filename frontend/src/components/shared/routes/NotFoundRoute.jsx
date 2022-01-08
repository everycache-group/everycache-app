import React from "react";
import { Route } from "react-router-dom";
import NotFound from "../../../pages/NotFound/NotFound";

const NotFoundRoute = () => {
  return <Route path="*" component={NotFound} />;
};

export default NotFoundRoute;
