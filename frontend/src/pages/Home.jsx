import React from "react";
import PageWrapper from "./../components/common/wrappers/PageWrapper";
import { logoutUser } from "../redux/slices/authSlice";
import { useDispatch } from "react-redux";

const Home = () => {
  const dispatch = useDispatch();

  const onClickHandler = (e) => {
    e.preventDefault();
    dispatch(logoutUser());
  };

  return (
    <PageWrapper>
      <button onClick={onClickHandler}> logout</button>
    </PageWrapper>
  );
};

export default Home;
