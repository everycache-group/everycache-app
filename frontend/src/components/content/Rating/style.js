import styled from "styled-components";

export const RatingWrapper = styled.div`
  height: 70px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  border: 1px solid #ccc;
  padding: 16px;
`;

export const CacheFormWrapper = styled.div`
  border: 1px solid #ccc;
  height: 600px;
  padding: 16px;
  border-radius: 25px;
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-between;
`;

export const CacheFormContent = styled.div`
  height: 100%;
  display: flex;
  flex-wrap: nowrap;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 25px 16px 25px 0;
  width: 250px;
`;

export const CacheInputWrapper = styled.div`
  display: flex;
  flex-wrap: nowrap;
  flex-direction: column;
  height: 50%;
  row-gap: 15px;
`;

export const CacheCoordsWrapper = styled.div`
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  gap: 16px;
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
`;

export const MarkerLocationWrapper = styled.div`
  z-index: 500;
  position: absolute;
  top: 80px;
  width: 33px;
  height: 33px;
  left: 10px;
  background-color: #fff;
  border-radius: 2px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  text-align: center;
  color: black;
  cursor: pointer;
  text-decoration: none;

  &:hover {
    background-color: #e7eadb;
    opacity: none;
  }
`;
