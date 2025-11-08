module Main exposing (main)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode as D
import Json.Encode as E


-- MAIN


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }


-- MODEL


type alias Model =
    { blockNumber : String
    , balance : String
    , gasPrice : String
    , address : String
    , status : Status
    }


type Status
    = Init
    | Loading
    | Success
    | Failure String


init : () -> ( Model, Cmd Msg )
init _ =
    ( { blockNumber = ""
      , balance = ""
      , gasPrice = ""
      , address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
      , status = Init
      }
    , Cmd.none
    )


-- UPDATE


type Msg
    = GetBlockNumber
    | GotBlockNumber (Result Http.Error String)
    | GetBalance
    | GotBalance (Result Http.Error String)
    | GetGasPrice
    | GotGasPrice (Result Http.Error String)
    | UpdateAddress String


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GetBlockNumber ->
            ( { model | status = Loading }
            , rpcCall "eth_blockNumber" [] GotBlockNumber
            )

        GotBlockNumber result ->
            case result of
                Ok blockNum ->
                    ( { model | blockNumber = hexToDecimal blockNum, status = Success }
                    , Cmd.none
                    )

                Err _ ->
                    ( { model | status = Failure "Failed to get block number" }
                    , Cmd.none
                    )

        GetBalance ->
            ( { model | status = Loading }
            , rpcCall "eth_getBalance" [ model.address, "latest" ] GotBalance
            )

        GotBalance result ->
            case result of
                Ok balance ->
                    ( { model | balance = weiToEther balance, status = Success }
                    , Cmd.none
                    )

                Err _ ->
                    ( { model | status = Failure "Failed to get balance" }
                    , Cmd.none
                    )

        GetGasPrice ->
            ( { model | status = Loading }
            , rpcCall "eth_gasPrice" [] GotGasPrice
            )

        GotGasPrice result ->
            case result of
                Ok gasPrice ->
                    ( { model | gasPrice = weiToGwei gasPrice, status = Success }
                    , Cmd.none
                    )

                Err _ ->
                    ( { model | status = Failure "Failed to get gas price" }
                    , Cmd.none
                    )

        UpdateAddress newAddress ->
            ( { model | address = newAddress }
            , Cmd.none
            )


-- HTTP


rpcCall : String -> List String -> (Result Http.Error String -> msg) -> Cmd msg
rpcCall method params toMsg =
    Http.post
        { url = "https://mainnet.infura.io/v3/YOUR_KEY"
        , body =
            Http.jsonBody <|
                E.object
                    [ ( "jsonrpc", E.string "2.0" )
                    , ( "id", E.int 1 )
                    , ( "method", E.string method )
                    , ( "params", E.list E.string params )
                    ]
        , expect = Http.expectJson toMsg rpcDecoder
        }


rpcDecoder : D.Decoder String
rpcDecoder =
    D.field "result" D.string


-- HELPERS


hexToDecimal : String -> String
hexToDecimal hex =
    hex
        |> String.dropLeft 2
        |> String.toInt
        |> Maybe.withDefault 0
        |> String.fromInt


weiToEther : String -> String
weiToEther wei =
    let
        weiInt =
            wei
                |> String.dropLeft 2
                |> String.toInt
                |> Maybe.withDefault 0

        ether =
            toFloat weiInt / 1.0e18
    in
    String.fromFloat ether


weiToGwei : String -> String
weiToGwei wei =
    let
        weiInt =
            wei
                |> String.dropLeft 2
                |> String.toInt
                |> Maybe.withDefault 0

        gwei =
            toFloat weiInt / 1.0e9
    in
    String.fromFloat gwei


-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none


-- VIEW


view : Model -> Html Msg
view model =
    div [ class "container" ]
        [ h1 [] [ text "Elm Web3 Client" ]
        , div [ class "info" ]
            [ p [] [ text ("Block Number: " ++ model.blockNumber) ]
            , button [ onClick GetBlockNumber ] [ text "Get Block Number" ]
            ]
        , div [ class "info" ]
            [ input
                [ type_ "text"
                , placeholder "Ethereum Address"
                , value model.address
                , onInput UpdateAddress
                ]
                []
            , p [] [ text ("Balance: " ++ model.balance ++ " ETH") ]
            , button [ onClick GetBalance ] [ text "Get Balance" ]
            ]
        , div [ class "info" ]
            [ p [] [ text ("Gas Price: " ++ model.gasPrice ++ " Gwei") ]
            , button [ onClick GetGasPrice ] [ text "Get Gas Price" ]
            ]
        , viewStatus model.status
        ]


viewStatus : Status -> Html Msg
viewStatus status =
    case status of
        Init ->
            text ""

        Loading ->
            p [] [ text "Loading..." ]

        Success ->
            p [ class "success" ] [ text "Success!" ]

        Failure error ->
            p [ class "error" ] [ text ("Error: " ++ error) ]
