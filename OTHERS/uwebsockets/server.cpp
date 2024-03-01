#include <uWS/uWS.h>
#include <iostream>

extern "C" void startWebSocketServer(int port) {
    uWS::Hub hub;

    hub.onMessage([](uWS::WebSocket<uWS::SERVER> ws, char *message, size_t length, uWS::OpCode opCode) {
        // Echo back the received message
        ws.send(message, length, opCode);
    });

    hub.onConnection([](uWS::WebSocket<uWS::SERVER> ws, uWS::HttpRequest req) {
        std::cout << "Client connected" << std::endl;
    });

    hub.onDisconnection([](uWS::WebSocket<uWS::SERVER> ws, int code, char *message, size_t length) {
        std::cout << "Client disconnected" << std::endl;
    });

    if (hub.listen(port)) {
        std::cout << "Server listening on port " << port << std::endl;
    } else {
        std::cerr << "Failed to listen on port " << port << std::endl;
        return;
    }

    hub.run();
}
