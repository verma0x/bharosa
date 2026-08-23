import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class TrustForgeServer {

    public static void main(
            String[] args
    ) throws Exception {

        HttpServer server =
                HttpServer.create(
                        new InetSocketAddress(
                                8080
                        ),
                        0
                );


        server.createContext(
                "/health",
                TrustForgeServer::health
        );


        server.createContext(
                "/verify",
                TrustForgeServer::verify
        );


        server.start();


        System.out.println(
                "TrustForge Java Server running on port 8080"
        );

    }


    private static void health(
            HttpExchange exchange
    ) throws IOException {

        send(
                exchange,
                "{"
                + "\"status\":\"running\","
                + "\"application\":\"TrustForge\""
                + "}"
        );

    }


    private static void verify(
            HttpExchange exchange
    ) throws IOException {

        send(
                exchange,
                "{"
                + "\"verified\":true,"
                + "\"message\":\"Identity verified\""
                + "}"
        );

    }


    private static void send(
            HttpExchange exchange,
            String response
    ) throws IOException {

        byte[] data =
                response.getBytes();


        exchange.getResponseHeaders()
                .set(
                    "Content-Type",
                    "application/json"
                );


        exchange.sendResponseHeaders(
                200,
                data.length
        );


        try (
            OutputStream output =
                exchange.getResponseBody()
        ) {

            output.write(data);

        }

    }
}