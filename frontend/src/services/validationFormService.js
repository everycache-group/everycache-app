const validate = (values) => {
  let errors = {};

  checkForEmptyFields(values, errors);

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

const checkForEmptyFields = (values, errors) => {
  for (const key in values) {
    const element = values[key];

    if (!element) {
      Object.defineProperty(errors, key, {
        value: `${key} is required`,
        writable: true,
        enumerable: true, //FUNNY BUG WHEN REMOVING XD
      });
    }
  }
};

const checkField = (values, errors, key, condition, msgOnFail) => {
  if (values.hasOwnProperty(key) && !errors[key]) {
    if (!condition) errors[key] = msgOnFail;
  }
};

export default validate;
