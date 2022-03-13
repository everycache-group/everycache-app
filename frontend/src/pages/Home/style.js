import styled from "styled-components";

export const HomeContainer = styled.div`
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  row-gap: 45px;
  background-color: #15171c;
  margin: 0 30px;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.32);
  padding: 60px;
  min-width: 500px;
  max-width: 1300px;
  color: #e1e9fc;
`;

export const Header = styled.h2`
  font-size: 70px;
`;

export const HomeContent = styled.div`
  display: flex;
  column-gap: 45px;
  align-items: center;
  justify-content: center;
`;

export const CacheImage = styled.img`
  border-radius: 100%;
`;

export const WelcomeText = styled.p`
  font-size: 40px;
  text-align: justify;
  line-height: 1.4;
`;
