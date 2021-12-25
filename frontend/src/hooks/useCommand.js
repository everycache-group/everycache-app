import { logoutUser } from "../redux/slices/authSlice";
import { useDispatch } from "react-redux";

const useCommand = (commandName) => {
  const dispatch = useDispatch();

  const runCommand = (e) => {
    e.preventDefault();
    switch (commandName) {
      case commands.logout:
        dispatch(logoutUser());
        break;
    }
  };

  return { runCommand };
};

export const commands = {
  logout: "logout",
};

export default useCommand;
