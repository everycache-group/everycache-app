import React from "react";
import { compose } from "react-recompose";
import withPageWrapper from "../../hoc/withPageWrapper";
import * as Style from "./style.js";

const Home = () => {
  return (
    <Style.HomeContainer>
      <Style.Header>Welcome on Gocache App!</Style.Header>
      <Style.HomeContent>
        <Style.CacheImage src="/images/HomeImage.jpg" />
        <Style.WelcomeText>
          Geocaching is a real-world, outdoor adventure that is happening all
          the time, all around the world. To play, participants use the
          Geocaching app and/or a GPS device to navigate to cleverly hidden
          containers called geocaches.
        </Style.WelcomeText>
      </Style.HomeContent>
    </Style.HomeContainer>
  );
};

export default compose(withPageWrapper)(Home);
