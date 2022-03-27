# Unified system of shops

# There is a [mobile app](https://github.com/zovenor/UniSS_mobile_app) for this system

## REST API

* [Get Token](#get-token)
* [Create an application token](#create-an-application-token)
* [Get chains](#get-chains)
* [Get shops](#get-shops)
* [Create a shop](#create-a-shop)
* [Delete a shop](#delete-a-shop)
* [Update a shop](#update-a-shop)
* [Get managers](#get-managers)
* [Add a manager](#add-a-manager)
* [Remove a manager](#remove-a-manager)
* [Get products](#get-products)
* [Add a product](#add-a-product)
* [Delete a product](#delete-a-product)
* [Update a product](#update-a-product)
* [Add to the count in the product](#add-to-the-count-in-the-product)

* ## Get Token
#### POST `/api/v1/token/`
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body:
```yaml
  {
  username: <USERNAME (type:str) (REQUIRED)>,
  password: <PASSWORD (type:str) (REQUIRED)>,
}
```
#### Response:
```yaml 
{
  token: <USER_TOKEN (type:str)>,
}
```
* ## Create an application token
#### POST `/api/v1/create_app_token/`
#### Headers
```yaml
{
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  name: <UNIQUE_NAME (type:str) (REQUIRED)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
}
```
* ## Get shops around
#### GET `/api/v1/shops_around/`
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  lat: <LATITUDE (type:float) (REQUIRED)>,
  lng: <LONGTUDE (type:float) (REQUIRED)>,
  radius: <RADIUS (type:float) (km, default:0.5)>
}
```
#### Response
```yaml
{
  shops: [
    ...
    {
      id: <ID_OF_SHOP (type:int)>,
      lat: <LATITUDE (type:float)>,
      lng: <LONGTUDE (type:float)>,
      chain: <CHAIN_OF_SHOP_ID (type:int)>,
      managers: [
        ...
        <USER_ID (type:int)>,
        ...
      ]
    }
    ...
  ]
}
```
* ## Get chains
#### GET `/api/v1/chains/`
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  id: <CHAIN_ID (type:int)>,
}
```
#### Response
```yaml
{
  chains: [
    ...
    {
      id: <ID (type:int)>,
      name: <NAME (type:str)>,
      unique_name: <UNIQUE_NAME (type:str)>,
      description: <DESCRIPTION (type:str)>,
      managers: [
        ...
        <MANAGER_ID (type:int)>,
        ...
      ],
    }
    ...
  ],
}
```
* ## Get shops
#### GET `/api/v1/shops/`
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  chain: <CHAIN_OF_SHOPS_ID (type:int)>,
  id: <SHOP_ID (type:int)>,
}
```
#### Response
```yaml
{
  shops: [
    ...
    {
      id: <SHOP_ID (type:int)>,
      lat: <LATITUDE (type:float)>,
      lng: <LONGTUDE (type:float)>,
      chain: <CHAIN__OF_SHOP_ID (type:int)>,
      managers: [
        ...
        <USER_ID (type:int)>,
        ...
      ]
    }
    ...
  ]
}
```
* ## Create a shop
#### POST `/api/v1/shops/`
#### Permissions
You should be a manager of this shop chain
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  chain:  <CHAIN_ID (type:int) (REQUIRED)>,
  lat: <LATITUDE (type:float) (REQUIRED)>,
  lng: <LONGTUDE (type:float) (REQUIRED)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
  shop: {
    id: <SHOP_ID (type:int)>,
    lat: <LATITUDE (type:float)>,
    lng: <LONGTUDE (type:float)>,
    chain: <CHAIN_OF_SHOP_ID (type:int)>,
    managers: [
      ...
      <USER_ID (type:int)>,
      ...
    ]
  }
}
```
* ## Delete a shop
#### DELETE `/api/v1/shops/`
#### Permissions
You should be a manager of this shop chain
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  id: <SHOP_ID (type:int) (REQUIRED)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
}
```
* ## Update a shop
#### PATCH `/api/v1/shops/`
#### Permissions
You should be a manager of this shop chain
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  id: <SHOP_ID (type:int) (REQUIRED)>,
  chain: <CHAIN_ID (type:int)>,
  lat: <LATITUDE (type:float)>,
  lng: <LONGTUDE (type:float)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
  shop: {
    id: <SHOP_ID (type:int)>,
    lat: <LATITUDE (type:float)>,
    lng: <LONGTUDE (type:float)>,
    chain: <CHAIN_OF_SHOP_ID (type:int)>,
    managers: [
      ...
      <USER_ID (type:int)>,
      ...
    ]
  }
}
```
* ## Get managers
#### GET `/api/v1/managers/`
#### Headers
```yaml
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
  type: <TYPE (type:str) ('chain' or 'shop') (REQUIRED)>
  id: <SHOP_ID (type:int) (REQUIRED)>,
```
#### Response
```yaml
{
  managers: [
    ...
      {
        id: <USER_ID (type:int)>,
        username: <USERNAME (type:str)>,
        first_name: <FIRST_NAME (type:str)>,
        last_name: <LAST_NAME (type:str)>,
        email: <EMAIL (type:str)>,
      }
    ...
  ]
}
```
* ## Add a manager
#### POST `/api/v1/managers/`
#### Permissions
You should be a manager of this shop or shop chain
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  type: <TYPE (type:str) ('chain' or 'shop') (REQUIRED)>
  id: <SHOP_ID (type:int) (REQUIRED)>,
  user: <USER_ID (type:int) (REQUIRED)>
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>
  manager: 
      {
        id: <USER_ID (type:int)>,
        username: <USERNAME (type:str)>,
        first_name: <FIRST_NAME (type:str)>,
        last_name: <LAST_NAME (type:str)>,
        email: <EMAIL (type:str)>,
      }
}
```
* ## Remove a manager
#### DELETE `/api/v1/managers/`
#### Permissions
You should be a manager of this shop or shop chain
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  type: <TYPE (type:str) ('chain' or 'shop') (REQUIRED)>
  id: <SHOP_ID (type:int) (REQUIRED)>,
  user: <USER_ID (type:int) (REQUIRED)>
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>
  manager: 
      {
        id: <USER_ID (type:int)>,
        username: <USERNAME (type:str)>,
        first_name: <FIRST_NAME (type:str)>,
        last_name: <LAST_NAME (type:str)>,
        email: <EMAIL (type:str)>,
      }
}
```
* ### Get products
#### GET `/api/v1/products/`
#### Query parameters
```
/api/v1/products?find=<FIND_TEXT (type:str)>
```
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  chain: <CHAIN_ID (type:int)>,
  shop: <SHOP_ID (type:int)>,
  id: <PRODUCT_ID (type:int),
}
```
#### Response
```yaml
{
  products: [
    ...
    {
      id: <ID (type:int)>,
      name: <NAME (type:str)>,
      price: <PRICE (type:float)>,
      currency: <CURRENCY (type:str)>,
      count: <COUNT (type:int)>,
      code: <CODE (type:int)>,
      shop: <ID_OF_SHOP (type:int)>,
    }
    ...
  ]
}
```
* ### Add a product
#### POST `api/v1/products/`
#### Permissions
You should be a manager of this shop or shop chain
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  shop: <SHOP_ID (type:int) (REQUIRED)>,
  name: <NAME (type:str) (REQUIRED)>,
  price: <PRICE (type:float) (REQUIRED)>,
  currecy: <CURRENCY (type:str) (REQUIRED)>,
  count: <COUNT (type:int) (REQUIRED)>,
  code: <CODE (type:int) (REQUIRED)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
  product: {
      id: <ID (type:int)>,
      name: <NAME (type:str)>,
      price: <PRICE (type:float)>,
      currency: <CURRENCY (type:str)>,
      count: <COUNT (type:int)>,
      code: <CODE (type:int)>,
      shop: <ID_OF_SHOP (type:int)>,
    }
}
```
* ### Delete a product
#### DELETE `/api/v1/products/`
#### Permissions
You should be a manager of this shop or shop chain
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
````yaml
{
  id: <ID (type:str) (REQUIRED)>,
}
````
##### Response
```yaml
{
  message: <MESSAGE (type:str)>,
}
```
* ### Update a product
#### PATCH `/api/v1/products/`
#### Permissions
You should be a manager of this shop or shop chain
#### Headers
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  id: <ID (type:str) (REQUIRED)>,
  name: <NAME (type:str),
  price: <PRICE (type:float)>,
  currecy: <CURRENCY (type:str)>,
  count: <COUNT (type:int)>,
  code: <CODE (type:int)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
  product: {
      id: <ID (type:int)>,
      name: <NAME (type:str)>,
      price: <PRICE (type:float)>,
      currency: <CURRENCY (type:str)>,
      count: <COUNT (type:int)>,
      code: <CODE (type:int)>,
      shop: <ID_OF_SHOP (type:int)>,
    }
}
```
* ### Add to the count in the product
#### Permissions
You should be a manager of this shop or shop chain
#### Header
```yaml
{
  App-Token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  Auth-Token: <USER_TOKEN (type:str) (REQUIRED)>,
}
```
#### Body
```yaml
{
  id: <ID (type:int) (REQUIRED)>,
  count: <COUNT_TO_ADD (type:int) (REQUIRED)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
  product: {
      id: <ID (type:int)>,
      name: <NAME (type:str)>,
      price: <PRICE (type:float)>,
      currency: <CURRENCY (type:str)>,
      count: <COUNT (type:int)>,
      code: <CODE (type:int)>,
      shop: <ID_OF_SHOP (type:int)>,
    }
}
```