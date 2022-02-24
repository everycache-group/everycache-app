import React, {
  useEffect
} from "react";
import {
  compose
} from "react-recompose";
import {
  useSelector,
  useDispatch
} from "react-redux";
import withPageWrapper from "../../hoc/withPageWrapper";
import {
  getUsers
} from "../../redux/slices/userSlice";
import UserTable from "../../components/shared/table/usertable/UserTable";
import UserMenu from "../../components/navigation/UserMenu/UserMenu";
import * as Style from "./style.js"

function UsersList() {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getUsers());
  }, []);

  const {
    users,
    role,
  } = useSelector((state) => state.user);

  return (
    <>
      <Style.UserContent >
        {role == "Admin" && < UserMenu / >}
        <UserTable data = {users}/>
      </Style.UserContent>
    </>
  );
}

export default compose(withPageWrapper)(UsersList);
