import React from "react";
import { compose } from "react-recompose";
import withPageWrapper from "../../hoc/withPageWrapper";
import * as Style from "./style.js";

const Home = () => {
  return (
    <div>
      <h2>Welcome on Gocache App!</h2>
      <img src="/images/HomeImage.jpg" />
      <p>
        Lorem, ipsum dolor sit amet consectetur adipisicing elit. Possimus
        incidunt, ex praesentium explicabo quaerat blanditiis, porro quae nobis
        expedita maiores qui laborum non rem. Magnam laudantium quidem eveniet
        rerum dignissimos! Lorem ipsum dolor sit, amet consectetur adipisicing
        elit. Placeat inventore veniam suscipit molestiae fugit esse ea ullam
        modi dolore sequi deleniti animi distinctio iusto, vitae, non, iste
        blanditiis asperiores maxime? Lorem ipsum dolor sit, amet consectetur
        adipisicing elit. Quae sequi distinctio eaque? Quidem in similique
        facere inventore hic, iste a numquam nihil non porro quas quod saepe est
        at sequi!
      </p>
    </div>
  );
};

export default compose(withPageWrapper)(Home);
