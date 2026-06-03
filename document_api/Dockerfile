# Stage 1: Build the application using the .NET SDK
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies
COPY ["./DocumentGenerator/DocumentGenerator.csproj", "./"]
RUN dotnet restore "./DocumentGenerator.csproj"
COPY ./DocumentGenerator .

# # Copy everything else and build the release
# COPY . .
# RUN dotnet build "DocumentGenerator.csproj" -c Release -o /app/build

# Stage 2: Create the runtime image using the ASP.NET Core Runtime
FROM build AS publish
RUN dotnet publish "DocumentGenerator.csproj" -c Release -o /app/publish


FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /app
COPY --from=publish /app/publish .
COPY ./DocumentGenerator/Assets ./Assets

# Expose the default port (.NET 8+ uses 8080 by default)
# EXPOSE 8080
ENTRYPOINT ["dotnet", "DocumentGenerator.dll"]
