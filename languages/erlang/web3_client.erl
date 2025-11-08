-module(web3_client).
-behaviour(gen_server).

%% API
-export([start_link/0, get_block_number/0, get_balance/1, get_gas_price/0]).

%% gen_server callbacks
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2]).

-define(RPC_URL, "https://mainnet.infura.io/v3/YOUR_KEY").

%%%===================================================================
%%% API
%%%===================================================================

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

get_block_number() ->
    gen_server:call(?MODULE, get_block_number).

get_balance(Address) ->
    gen_server:call(?MODULE, {get_balance, Address}).

get_gas_price() ->
    gen_server:call(?MODULE, get_gas_price).

%%%===================================================================
%%% gen_server callbacks
%%%===================================================================

init([]) ->
    {ok, #{rpc_url => ?RPC_URL}}.

handle_call(get_block_number, _From, State) ->
    Result = rpc_call("eth_blockNumber", []),
    {reply, Result, State};

handle_call({get_balance, Address}, _From, State) ->
    Result = rpc_call("eth_getBalance", [Address, <<"latest">>]),
    {reply, Result, State};

handle_call(get_gas_price, _From, State) ->
    Result = rpc_call("eth_gasPrice", []),
    {reply, Result, State}.

handle_cast(_Msg, State) ->
    {noreply, State}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

%%%===================================================================
%%% Internal functions
%%%===================================================================

rpc_call(Method, Params) ->
    Body = jsx:encode(#{
        <<"jsonrpc">> => <<"2.0">>,
        <<"id">> => 1,
        <<"method">> => list_to_binary(Method),
        <<"params">> => Params
    }),

    Headers = [{<<"Content-Type">>, <<"application/json">>}],

    case httpc:request(post, {?RPC_URL, Headers, "application/json", Body}, [], []) of
        {ok, {{_, 200, _}, _, ResponseBody}} ->
            case jsx:decode(list_to_binary(ResponseBody), [return_maps]) of
                #{<<"result">> := Result} -> {ok, Result};
                #{<<"error">> := Error} -> {error, Error};
                _ -> {error, invalid_response}
            end;
        {error, Reason} ->
            {error, Reason}
    end.
