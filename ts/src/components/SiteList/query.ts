import { gql } from 'apollo-boost'

export const QUERY_SITE_LIST = gql`
  query Sites($limit: Int, $within: String) {
    sites(limit: $limit, within: $within) {
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
