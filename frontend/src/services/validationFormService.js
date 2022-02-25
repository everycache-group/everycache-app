const validate = (values) => {
  let errors = {};

  for (const keyName of ["Email", "Name", "Username", "Description", "Password"]) {
    const key = keyName.toLowerCase();
    checkField(
      values,
      errors,
      key,
      values[key] !== undefined && values[key].length,
      `${keyName} field cannot be empty.`
    );
  }

  checkField(
    values,
    errors,
    "email",
    /\S+@\S+\.\S+/.test(values.email),
    "Email is invalid."
  );

  checkField(
    values,
    errors,
    "username",
      values.username !== undefined && values.username.length >= 5,
    "Username has to be at least 5 characters long."
  );

  checkField(
    values,
    errors,
    "description",
    values.description !== undefined && values.description.length >= 5,
    "Description has to be at least 5 characters long."
  );

  checkField(
    values,
    errors,
    "name",
    values.name !== undefined && values.name.length >= 5,
    "Name has to be at least 5 characters long."
  );

  checkField(
    values,
    errors,
    "password",
    values.password !== undefined && values.password.length >= 8 && values.password.length <= 255,
    "Password length has to be greater than 8 and lower than 255."
  );

  checkField(
    values,
    errors,
    "password2",
    values.password === values.password2,
    "Both passwords must be equal."
  );

  checkField(
    values,
    errors,
    "lat",
    values.lat >= -90 && values.lat <= 90,
    "Latitude must be in range from -90 to 90 degrees"
  );

  checkField(
    values,
    errors,
    "lng",
    values.lng >= -180 && values.lng <= 180,
    "Longitude must be in range from -180 to 180 degrees"
  );

  return errors;
};

const checkField = (values, errors, key, condition, msgOnFail) => {
  if (values.hasOwnProperty(key) && !errors[key]) {
    if (!condition) errors[key] = msgOnFail;
  }
};

export default validate;
