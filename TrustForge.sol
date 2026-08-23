/ SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TrustForge {

    address public admin;

    struct Organization {
        string name;
        string serviceURL;
        bool verified;
        bool revoked;
    }

    uint256 public organizationCount;

    mapping(uint256 => Organization) public organizations;

    event OrganizationRegistered(
        uint256 indexed id,
        string name,
        string serviceURL
    );

    event OrganizationRevoked(
        uint256 indexed id
    );

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin allowed");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function registerOrganization(
        string memory _name,
        string memory _serviceURL
    ) public onlyAdmin {

        organizationCount++;

        organizations[organizationCount] = Organization(
            _name,
            _serviceURL,
            true,
            false
        );

        emit OrganizationRegistered(
            organizationCount,
            _name,
            _serviceURL
        );
    }

    function revokeOrganization(
        uint256 _id
    ) public onlyAdmin {

        require(
            organizations[_id].verified,
            "Organization not found"
        );

        organizations[_id].verified = false;
        organizations[_id].revoked = true;

        emit OrganizationRevoked(_id);
    }

    function verifyOrganization(
        uint256 _id
    )
        public
        view
        returns (
            string memory,
            string memory,
            bool,
            bool
        )
    {
        Organization memory org =
            organizations[_id];

        return (
            org.name,
            org.serviceURL,
            org.verified,
            org.revoked
        );
    }
}