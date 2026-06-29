using System;
using System.Linq;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        string thumbprint = "BDC7248A63562FA33A3FEACE8C4980366EBF10F7";

        string message =
            args.Length > 0
            ? args[0]
            : "Sandhya Chandel";

        X509Store store =
            new X509Store(
                StoreName.My,
                StoreLocation.CurrentUser
            );

        store.Open(OpenFlags.ReadOnly);

        var cert =
            store.Certificates
                 .Find(
                    X509FindType.FindByThumbprint,
                    thumbprint,
                    false
                 )
                 .OfType<X509Certificate2>()
                 .FirstOrDefault();

        if (cert == null)
        {
            Console.WriteLine("Certificate not found");
            return;
        }

        if (!cert.HasPrivateKey)
        {
            Console.WriteLine("No private key");
            return;
        }

        using RSA? rsa = cert.GetRSAPrivateKey();

        if (rsa == null)
        {
            Console.WriteLine("Unable to access TPM private key.");
            return;
        }

        byte[] data =
            Encoding.UTF8.GetBytes(message);

        byte[] signature =
            rsa.SignData(
                data,
                HashAlgorithmName.SHA256,
                RSASignaturePadding.Pkcs1
            );

        Console.WriteLine(
            Convert.ToBase64String(signature)
        );
    }
}
