import {
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import * as Style from "./style";
import PropTypes from "prop-types";
import CollapsedRow from "../collapsedRow/CollapsedRow";

function CacheTable({ title, header, data }) {
  const collapsedRowHeader = header.details;

  const mainHeader = Object.values(header).filter(
    (prop) => typeof prop == "string"
  );

  return (
    <Style.StyledTableWrapper>
      <TableContainer component={Paper}>
        <Table>
          {/* HEADER TABLE*/}

          <TableHead>
            <TableRow>
              <TableCell>
                <Typography variant="h5" gutterBottom borderBottom={2}>
                  {title}
                </Typography>
              </TableCell>
              {mainHeader.map((element) => (
                <TableCell
                  key={element}
                  align="right"
                  sx={{ fontSize: "18px" }}
                >
                  {element}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>

          <TableBody>
            {data.map((row) => (
              <CollapsedRow
                key={row.cacheId}
                header={collapsedRowHeader}
                data={row}
              />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Style.StyledTableWrapper>
  );
}

CacheTable.propTypes = {
  title: PropTypes.string.isRequired,
  header: PropTypes.object.isRequired,
  data: PropTypes.array.isRequired,
};

export default CacheTable;
