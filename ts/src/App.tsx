import React from 'react';
import logo from './logo.svg';
import './App.css';
import {Box, Flex, Text} from "rebass";

import FullScreenMap from "./map"
import {NavigationControl} from "react-map-gl";

require('dotenv').config();


const App: React.FC = () => {
  return (
      <FullScreenMap>
          <Flex>
              <Text>Welcome to Digmaps!</Text>
          </Flex>
      </FullScreenMap>
  );
};

export default App;
