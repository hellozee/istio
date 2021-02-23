// Code generated by protoc-gen-go. DO NOT EDIT.
// source: meshca.proto

package google_security_meshca_v1

import (
	context "context"
	fmt "fmt"
	proto "github.com/golang/protobuf/proto"
	duration "github.com/golang/protobuf/ptypes/duration"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	math "math"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion3 // please upgrade the proto package

// Certificate request message.
type MeshCertificateRequest struct {
	// The request ID must be a valid UUID with the exception that zero UUID is
	// not supported (00000000-0000-0000-0000-000000000000).
	RequestId string `protobuf:"bytes,1,opt,name=request_id,json=requestId,proto3" json:"request_id,omitempty"`
	// PEM-encoded certificate request.
	Csr string `protobuf:"bytes,2,opt,name=csr,proto3" json:"csr,omitempty"`
	// Optional: requested certificate validity period.
	Validity             *duration.Duration `protobuf:"bytes,3,opt,name=validity,proto3" json:"validity,omitempty"`
	XXX_NoUnkeyedLiteral struct{}           `json:"-"`
	XXX_unrecognized     []byte             `json:"-"`
	XXX_sizecache        int32              `json:"-"`
}

func (m *MeshCertificateRequest) Reset()         { *m = MeshCertificateRequest{} }
func (m *MeshCertificateRequest) String() string { return proto.CompactTextString(m) }
func (*MeshCertificateRequest) ProtoMessage()    {}
func (*MeshCertificateRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_5692c9cb61f5c10e, []int{0}
}

func (m *MeshCertificateRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_MeshCertificateRequest.Unmarshal(m, b)
}
func (m *MeshCertificateRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_MeshCertificateRequest.Marshal(b, m, deterministic)
}
func (m *MeshCertificateRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_MeshCertificateRequest.Merge(m, src)
}
func (m *MeshCertificateRequest) XXX_Size() int {
	return xxx_messageInfo_MeshCertificateRequest.Size(m)
}
func (m *MeshCertificateRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_MeshCertificateRequest.DiscardUnknown(m)
}

var xxx_messageInfo_MeshCertificateRequest proto.InternalMessageInfo

func (m *MeshCertificateRequest) GetRequestId() string {
	if m != nil {
		return m.RequestId
	}
	return ""
}

func (m *MeshCertificateRequest) GetCsr() string {
	if m != nil {
		return m.Csr
	}
	return ""
}

func (m *MeshCertificateRequest) GetValidity() *duration.Duration {
	if m != nil {
		return m.Validity
	}
	return nil
}

// Certificate response message.
type MeshCertificateResponse struct {
	// PEM-encoded certificate chain.
	// Leaf cert is element '0'. Root cert is element 'n'.
	CertChain            []string `protobuf:"bytes,1,rep,name=cert_chain,json=certChain,proto3" json:"cert_chain,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *MeshCertificateResponse) Reset()         { *m = MeshCertificateResponse{} }
func (m *MeshCertificateResponse) String() string { return proto.CompactTextString(m) }
func (*MeshCertificateResponse) ProtoMessage()    {}
func (*MeshCertificateResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_5692c9cb61f5c10e, []int{1}
}

func (m *MeshCertificateResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_MeshCertificateResponse.Unmarshal(m, b)
}
func (m *MeshCertificateResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_MeshCertificateResponse.Marshal(b, m, deterministic)
}
func (m *MeshCertificateResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_MeshCertificateResponse.Merge(m, src)
}
func (m *MeshCertificateResponse) XXX_Size() int {
	return xxx_messageInfo_MeshCertificateResponse.Size(m)
}
func (m *MeshCertificateResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_MeshCertificateResponse.DiscardUnknown(m)
}

var xxx_messageInfo_MeshCertificateResponse proto.InternalMessageInfo

func (m *MeshCertificateResponse) GetCertChain() []string {
	if m != nil {
		return m.CertChain
	}
	return nil
}

func init() {
	proto.RegisterType((*MeshCertificateRequest)(nil), "google.security.meshca.v1.MeshCertificateRequest")
	proto.RegisterType((*MeshCertificateResponse)(nil), "google.security.meshca.v1.MeshCertificateResponse")
}

func init() { proto.RegisterFile("meshca.proto", fileDescriptor_5692c9cb61f5c10e) }

var fileDescriptor_5692c9cb61f5c10e = []byte{
	// 254 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x94, 0x90, 0xc1, 0x4a, 0xc3, 0x40,
	0x10, 0x86, 0x5d, 0x03, 0x62, 0x57, 0x0f, 0xba, 0x07, 0x4d, 0x0b, 0x4a, 0xc8, 0xa9, 0xa7, 0x2d,
	0x8d, 0x08, 0xde, 0xe3, 0xc5, 0x83, 0x97, 0xf8, 0x00, 0x65, 0xbb, 0x99, 0x36, 0x03, 0x35, 0x5b,
	0x67, 0x27, 0x81, 0x82, 0x07, 0x9f, 0xc2, 0xe7, 0x95, 0x4d, 0xa2, 0x08, 0xd5, 0x43, 0x6f, 0xc3,
	0xf7, 0xcf, 0x30, 0xdf, 0x8c, 0x3c, 0x7f, 0x05, 0x5f, 0x59, 0xa3, 0xb7, 0xe4, 0xd8, 0xa9, 0xf1,
	0xda, 0xb9, 0xf5, 0x06, 0xb4, 0x07, 0xdb, 0x10, 0xf2, 0x4e, 0x0f, 0x69, 0x3b, 0x9f, 0xdc, 0xf6,
	0xd1, 0xac, 0x6b, 0x5c, 0x36, 0xab, 0x59, 0xd9, 0x90, 0x61, 0x74, 0x75, 0x3f, 0x9a, 0x7e, 0x08,
	0x79, 0xf5, 0x0c, 0xbe, 0xca, 0x81, 0x18, 0x57, 0x68, 0x0d, 0x43, 0x01, 0x6f, 0x0d, 0x78, 0x56,
	0x37, 0x52, 0x52, 0x5f, 0x2e, 0xb0, 0x8c, 0x45, 0x22, 0xa6, 0xa3, 0x62, 0x34, 0x90, 0xa7, 0x52,
	0x5d, 0xc8, 0xc8, 0x7a, 0x8a, 0x8f, 0x3b, 0x1e, 0x4a, 0x75, 0x2f, 0x4f, 0x5b, 0xb3, 0xc1, 0x12,
	0x79, 0x17, 0x47, 0x89, 0x98, 0x9e, 0x65, 0x63, 0x3d, 0x98, 0x7d, 0xaf, 0xd7, 0x8f, 0xc3, 0xfa,
	0xe2, 0xa7, 0x35, 0x7d, 0x90, 0xd7, 0x7b, 0x06, 0x7e, 0xeb, 0x6a, 0x0f, 0x41, 0xc1, 0x02, 0xf1,
	0xc2, 0x56, 0x06, 0xeb, 0x58, 0x24, 0x51, 0x50, 0x08, 0x24, 0x0f, 0x20, 0xfb, 0xdc, 0x97, 0x7f,
	0x01, 0x6a, 0xd1, 0x82, 0x7a, 0x97, 0x97, 0x39, 0x81, 0x61, 0xf8, 0x95, 0xa9, 0xb9, 0xfe, 0xf7,
	0x51, 0xfa, 0xef, 0x27, 0x4c, 0xb2, 0x43, 0x46, 0x7a, 0xeb, 0xf4, 0x68, 0x79, 0xd2, 0xdd, 0x7b,
	0xf7, 0x15, 0x00, 0x00, 0xff, 0xff, 0xd9, 0x04, 0x17, 0xc7, 0xa7, 0x01, 0x00, 0x00,
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// MeshCertificateServiceClient is the client API for MeshCertificateService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type MeshCertificateServiceClient interface {
	// Using provided CSR, returns a signed certificate that represents a GCP
	// service account identity.
	CreateCertificate(ctx context.Context, in *MeshCertificateRequest, opts ...grpc.CallOption) (*MeshCertificateResponse, error)
}

type meshCertificateServiceClient struct {
	cc *grpc.ClientConn
}

func NewMeshCertificateServiceClient(cc *grpc.ClientConn) MeshCertificateServiceClient {
	return &meshCertificateServiceClient{cc}
}

func (c *meshCertificateServiceClient) CreateCertificate(ctx context.Context, in *MeshCertificateRequest, opts ...grpc.CallOption) (*MeshCertificateResponse, error) {
	out := new(MeshCertificateResponse)
	err := c.cc.Invoke(ctx, "/google.security.meshca.v1.MeshCertificateService/CreateCertificate", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// MeshCertificateServiceServer is the server API for MeshCertificateService service.
type MeshCertificateServiceServer interface {
	// Using provided CSR, returns a signed certificate that represents a GCP
	// service account identity.
	CreateCertificate(context.Context, *MeshCertificateRequest) (*MeshCertificateResponse, error)
}

// UnimplementedMeshCertificateServiceServer can be embedded to have forward compatible implementations.
type UnimplementedMeshCertificateServiceServer struct {
}

func (*UnimplementedMeshCertificateServiceServer) CreateCertificate(ctx context.Context, req *MeshCertificateRequest) (*MeshCertificateResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreateCertificate not implemented")
}

func RegisterMeshCertificateServiceServer(s *grpc.Server, srv MeshCertificateServiceServer) {
	s.RegisterService(&_MeshCertificateService_serviceDesc, srv)
}

func _MeshCertificateService_CreateCertificate_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MeshCertificateRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MeshCertificateServiceServer).CreateCertificate(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/google.security.meshca.v1.MeshCertificateService/CreateCertificate",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MeshCertificateServiceServer).CreateCertificate(ctx, req.(*MeshCertificateRequest))
	}
	return interceptor(ctx, in, info, handler)
}

var _MeshCertificateService_serviceDesc = grpc.ServiceDesc{
	ServiceName: "google.security.meshca.v1.MeshCertificateService",
	HandlerType: (*MeshCertificateServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "CreateCertificate",
			Handler:    _MeshCertificateService_CreateCertificate_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "meshca.proto",
}