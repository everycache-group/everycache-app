import React from "react";
import * as Style from "./style";

const Error = ({ message }) => {
  return (
    <Style.ErrorContainer>
      <p>Error: {message}</p>
    </Style.ErrorContainer>
  );
};

export default Error;
