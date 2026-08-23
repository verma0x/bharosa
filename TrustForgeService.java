import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

public class TrustForgeService {

    public static String createHash(
            String identity,
            String salt
    ) throws Exception {

        String input =
                identity + ":" + salt;

        MessageDigest md =
                MessageDigest.getInstance(
                        "SHA-256"
                );

        byte[] hash =
                md.digest(
                        input.getBytes(
                                StandardCharsets.UTF_8
                        )
                );

        StringBuilder result =
                new StringBuilder();

        for (byte b : hash) {

            result.append(
                    String.format(
                            "%02x",
                            b
                    )
            );
        }

        return result.toString();
    }


    public static String createCredentialId(
            String identity
    ) throws Exception {

        String hash =
                createHash(
                        identity,
                        "TRUSTFORGE"
                );

        return hash.substring(
                0,
                16
        );
    }


    public static boolean isTrusted(
            boolean verified,
            boolean revoked
    ) {

        return verified && !revoked;
    }


    public static void main(
            String[] args
    ) throws Exception {

        String credential =
                createCredentialId(
                        "DEMO-USER-001"
                );

        System.out.println(
                "TrustForge Credential ID: "
                + credential
        );

    }
}