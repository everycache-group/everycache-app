import React, {
  useEffect
} from "react";
import {
  compose
} from "react-recompose";
// import LeafletMap from "./../../components/content/map/LeafletMap";
// import SettingsMapTracker from "../../components/content/map/SettingsMapTracker";
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
// import CacheMarker from "../../components/content/cacheMarker/CacheMarker";
// import CacheTable from "../../components/shared/table/cachetable/CacheTable";

//import ResourceConnector from "../../services/resourceService";
//import config from "./../../api/api-config.json";
//const user = new ResourceConnector(config.resources.user);

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
