import TableCell from "@mui/materialTableCell";
import IconButton from "@mui/material/IconButton";
import Collapse from "@mui/material/Collapse";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";

import TableRow from "@mui/material/TableRow";
import React, { useState } from "react";
import PropTypes from "prop-types";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";

function CollapsedRow(props) {
  const [open, setOpen] = useState(false);
  const [data, setData] = useState(props.data);

  const collapsedRowData = data.details;
  const cells = Object.values(data).filter((item) => !(item instanceof Array));

  return (
    <>
      <TableRow sx={{ "& > *": { borderBottom: "unset" } }}>
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        {cells.map((cell) => (
          <TableCell key={cell.toString()} align="right">
            {cell}
          </TableCell>
        ))}
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              <Typography variant="h6" gutterBottom component="div">
                Details
              </Typography>
              <Box sx={{ border: "1px solid black" }}>
                <TextField
                  InputProps={{
                    readOnly: true,
                  }}
                  variant="standard"
                  id="creationDate"
                  multiline
                >
                  XD
                </TextField>
              </Box>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
}

CollapsedRow.propTypes = {
  header: PropTypes.array.isRequired,
  data: PropTypes.object.isRequired,
};

export default CollapsedRow;
