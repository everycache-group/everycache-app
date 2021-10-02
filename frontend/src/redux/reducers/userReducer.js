const initialState = {
    username: "lolol",

    isAuth: true,

   
};

function userReducer(state = initialState, action)
{
    switch(action.type)
    {
        

        default:
            return state;
    }
}

export default userReducer;