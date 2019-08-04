import { gql } from 'apollo-boost'

export const QUERY_SITE_LIST = gql`
  query Sites($limit: Int!) {
    sites(limit: $limit) {
      id
      modernName
      ancientName
      coordinates {
        x
        y
      }
    }
  }
`;
