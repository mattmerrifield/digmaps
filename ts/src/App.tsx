import React, {useState} from 'react';
import './App.css';
import {Box, Flex, Text} from "rebass";
import { Global } from "@emotion/core"

import Map from "./map"
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-boost';
import { ApolloProvider as ApolloHooksProvider } from 'react-apollo-hooks';
import {FaMapMarker} from "react-icons/fa";

import {useSitesQuery} from "./generated/graphql";
import {Marker} from "react-map-gl";


require('dotenv').config();

interface SiteMarkerProps{
 site: {
    modernName?: string
    coordinates: {
        x: number
        y: number
    }
}}


const client = new ApolloClient({uri: 'http://localhost:8000/api/'});


const App: React.FC = () => {
  return (
    <>
      <Global styles={{
        "html": {
          height: "100%"
        },
        "body": {
          height: "100%",
          display: "flex",
          flexDirection: "column"
        },
        "#root": {
          flex: "1 0 auto"
        }
      }}/>
      <ApolloProvider client={client}>
          <ApolloHooksProvider client={client}>
              <Flex flexDirection="row" height="100%">
                  <Box width={1} flex="1 0 auto">
                    <Map height="100%">
                          <Flex>
                              <Text>Welcome to Digmaps!</Text>
                          </Flex>
                      </Map>
                  </Box>
              </Flex>
          </ApolloHooksProvider>
      </ApolloProvider>
      </>
  );
};

export default App;
